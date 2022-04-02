import hashlib, httpx, ingest, json, logging, sys, time, traceback
from datetime import datetime, timezone
from sklearn.neighbors import KDTree

SN_URL = 'https://www.spotternetwork.org/feeds/reports.txt'
API_URL = 'http://localhost:8080/events'
HAZARD_MAP = ['?', 'tornado', 'funnel cloud', 'rotating wall cloud', 'hail', 'high wind', 'flooding', 'flash flood', 'other']

logging.basicConfig(filename='wx-sn.log', encoding='utf-8', level=logging.INFO)
client = httpx.Client(timeout=10.0)
with open('cities.json', 'r') as file:
    cities = json.loads(file.read())
cities_coords = [(x[0], x[1]) for x in cities]
cities_tree = KDTree(cities_coords)

# SN tends to have some non ascii chars in reports that should be removed
def strip_non_ascii(input):
    return ''.join(char for char in input if ord(char) < 128)

def get_ts(datestring):
    dt = datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S %Z')
    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp()) * 1000

def line_to_event(line):
    line = line[6:]
    splits = line.split('"Reported By: ')
    first_splits = splits[0].split(',')
    details = strip_non_ascii(splits[1])
    second_splits = details.split('\\n')
    hazard = HAZARD_MAP[int(first_splits[4])]
    event = {
        'report': {
            'hazard': hazard,
            'source': second_splits[0],
            'ts': get_ts(second_splits[2][6:]),
        },
        'ts': int(datetime.now().timestamp()) * 1000,
        'type': 'sn',
    }
    if hazard == 'hail':
        event['report']['mag'] = float(second_splits[3].split(' ')[1].replace('"', ''))
        event['report']['units'] = 'INCH'
    else:
        event['report']['notes'] = second_splits[3].replace('Notes: ', '')[:-1 or None]
    lat = float(first_splits[0])
    lon = float(first_splits[1])
    point = (lon, lat)
    nearest = ingest.get_nearest(point, cities_tree, cities)
    event['geo'] = {
        'point': point,
        'city': nearest[0],
        'st': nearest[1],
        'distance': nearest[2],
        'bearing': nearest[4]
    }
    return event

def get_reports(lastseen):
    new_lastseen = None
    events = []

    try:
        file = open('sample-data/sn', 'r')
        lines = file.read().split('\n')
        # resp = client.get(SN_URL)
        # lines = resp.text.split('\n')
        lines = [line.strip() for line in lines if line.strip() and 'Icon:' in line]
        
        new_lines = []
        # Lines are sorted by age descending, so you see the newest first
        for line in lines:
            hash = hashlib.md5(line.encode('utf-8')).hexdigest()
            if new_lastseen is None:
                new_lastseen = hash
            # Don't process everything on first load, wait for new events
            if lastseen is None:
                return (hash, [])
            if hash == lastseen:
                break
            new_lines.append(line)
        new_lines.reverse()

        for line in new_lines:
            events.append(line_to_event(line))
    except:
        logging.warning(traceback.format_exc())
    if new_lastseen is None:
        new_lastseen = lastseen
    return (new_lastseen, events)

last_seen = sys.argv[1] if len(sys.argv) > 1 else None
while (True):
    lastseen, events = get_reports(last_seen)
    ingest.publish_events(events)
    time.sleep(60)
