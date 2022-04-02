import httpx, ingest, json, logging, sys, time, traceback
from sklearn.neighbors import KDTree

BASE_URL = 'https://tgftp.nws.noaa.gov/SL.us008001/DF.c5/DC.textf/DS.torwf'

logging.basicConfig(filename='tor.log', encoding='utf-8', level=logging.INFO)
client = httpx.Client(timeout=10.0)
with open('cities.json', 'r') as file:
    cities = json.loads(file.read())
cities_coords = [(x[0], x[1]) for x in cities]
cities_tree = KDTree(cities_coords)

def process_file(filename):
    event = None
    try:
        url = f'{BASE_URL}/{filename}'
        resp = client.get(url)
        text = resp.text.replace('\r', '')
        emergency = 'TORNADO EMERGENCY' in text
        lines = text.split('\n')
        emergency_text = ''
        if emergency:
            for line in lines:
                if 'TORNADO EMERGENCY' in line:
                    emergency_text = line.strip().replace('.', '')
        wfo = lines[2][3:]
        text = lines[14].strip()
        for line in lines[15:]:
            if not line.strip():
                break
            text += line
        text = text.replace('  ', ' ')
        while text[-1] == '.':
            text = text[:-1]
        for line in lines:
            if 'TIME...MOT' in line:
                splits = line.strip().split(' ')
                lat = int(splits[-2]) / 100
                lon = (int(splits[-1]) / 100) * -1
                point = (lon, lat)
                break
        nearest = ingest.get_nearest(point, cities_tree, cities)

        event = {
            'geo': {
                'point': point,
                'city': nearest[0],
                'st': nearest[1],
                'distance': nearest[2],
                'bearing': nearest[4]
            },
            'emergency': emergency,
            'subject': text,
            'ts': ingest.get_ts_from_bulletin(lines[9]),
            'type': 'tor',
            'url': url,
            'wfo': wfo,
        }
        if emergency_text:
            event['subject2'] = emergency_text
    except:
        logging.warning(traceback.format_exc())
    return event

last_seen = sys.argv[1] if len(sys.argv) > 1 else None
while (True):
    url = f'{BASE_URL}/ls-lt' 
    last_seen, filenames = ingest.get_new_filenames(last_seen, url)
    if filenames:
        logging.info(f'Found {len(filenames)} new files')
    events = [process_file(x) for x in filenames]
    ingest.publish_events(events)
    time.sleep(60)
