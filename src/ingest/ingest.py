import httpx, logging, traceback
from datetime import datetime
from math import degrees, radians, cos, sin, asin, sqrt, atan2

API_URL = 'http://localhost:8080/events'

client = httpx.Client(timeout=10.0)

def get_nearest(point, tree, data):
    _, nearest_ind = tree.query([point], k=1)
    nearest = data[nearest_ind[0][0]]
    city = nearest[2]
    st = nearest[3]
    bearing = get_distance_and_bearing(nearest[1], nearest[0], point[1], point[0])
    return (city, st, bearing[0], bearing[1], bearing[2])

def get_bearing_direction(bearing):
    if bearing >= 337.5 or bearing < 22.5:
        return 'N'
    elif 22.5 <= bearing < 67.5:
        return 'NE'
    elif 67.5 <= bearing < 112.5:
        return 'E'
    elif 112.5 <= bearing < 157.5:
        return 'SE'
    elif 157.5 <= bearing < 202.5:
        return 'S'
    elif 202.5 <= bearing < 247.5:
        return 'SW'
    elif 247.5 <= bearing < 292.5:
        return 'W'
    else:
        return 'NW'

def get_distance_and_bearing(lat1, lon1, lat2, lon2):
    R = 3959.87433 # Earth radius in miles
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
    distance = round(R * c)
    bearing = atan2(sin(lon2-lon1) * cos(lat2), cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(lon2-lon1)))
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360
    direction = get_bearing_direction(bearing)
    return (distance, bearing, direction)

def get_coords(coords):
    parsed = []
    for i in range(0, len(coords), 2):
        lat = int(coords[i]) / 100
        lon = coords[i + 1]
        if lon[0] in ['0', '1', '2']:
            lon = '1' + lon
        lon = (int(lon) / 100) * -1
        parsed.append((lon, lat))
    return parsed

def code_to_offset(code):
    if code == 'EDT':
        return '-04:00'
    if code == 'EST':
        return '-05:00'
    elif code == 'MDT':
        return '-06:00'
    elif code == 'MST':
        return '-07:00'
    elif code == 'CST':
        return '-06:00'
    elif code == 'CDT':
        return '-05:00'
    elif code == 'PDT':
        return '-07:00'
    elif code == 'AST':
        return '−04:00'
    elif code == 'AKDT':
        return '-08:00'
    else:
        logging.info(f'Unknown timezone code "{code}"')
        return '-00:00'

def publish_events(events):
    events = [event for event in events if event]
    if events:
        try:
            client.post(API_URL, json=events)
        except Exception as e:
            logging.error(traceback.format_exc())

def get_ts_from_bulletin(date):
    date = date.split(' ')
    try:
        date = f'{date[6]}-{date[4]}-{date[5]} {date[0]} {date[1]} {code_to_offset(date[2])}'
        date = int(datetime.strptime(date, '%Y-%b-%d %I%M %p %z').timestamp()) * 1000
    except Exception as e:
        logging.warning(f'{e}: "{date}"')
    return date

def get_new_filenames(last_seen, url):
    try:
        resp = client.get(url)
        lines = resp.text.split('\n')
        lines.reverse()
        lines = [line for line in lines if line.strip()]
        latest = lines[-1].split(' ')[-1]

        # Stop processing if already up to date
        if last_seen == latest:
            return (latest, [])

        # If a fresh load, wait for new files to process
        if last_seen == None:
            return (latest, [])

        # Get new filenames
        new_files = []
        last_seen_passed = False
        for line in lines:
            filename = line.split(' ')[-1]
            if not last_seen_passed and filename == last_seen:
                last_seen_passed = True
                continue
            if last_seen_passed:
                new_files.append(filename)
        last_seen = latest
        return (latest, new_files)
    except Exception as e:
        logging.warning(traceback.format_exc())
        return (last_seen, [])
