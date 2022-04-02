import httpx, ingest, json, logging, sys, time, traceback
from datetime import datetime
from sklearn.neighbors import KDTree

LSR_URL = 'https://tgftp.nws.noaa.gov/SL.us008001/DF.c5/DC.textf/DS.lsrnw'
# Hazard types: NON-TSTM WND GST, SNOW, TSTM WND DMG, DENSE FOG, HAIL, TORNADO, FLASH FLOOD, HEAVY RAIN, MARINE TSTM WIND
# HEAVY SNOW, LIGHTNING, WATER SPOUT, DUST STORM, FREEZING RAIN, TSTM WND GST, FUNNEL CLOUD, WILDFIRE
TRACKED_HAZARDS = ['TORNADO', 'HAIL', 'FUNNEL CLOUD']
# LSRs can be days or even months old - ignore reports older than 15 minutes
MINUTES_THRESHOLD = 1500000 # TODO change back

logging.basicConfig(filename='wx-lsr.log', encoding='utf-8', level=logging.INFO)
client = httpx.Client(timeout=10.0)
with open('cities.json', 'r') as file:
    cities = json.loads(file.read())
cities_coords = [(x[0], x[1]) for x in cities]
cities_tree = KDTree(cities_coords)

def get_mag(raw_mag):
    try:
        if not raw_mag.strip():
            return (None, None, None)
        splits = [x.strip() for x in raw_mag.split(' ')]
        measured = True if splits[0][0] == 'M' else False
        units = splits[1].lower()
        mag = float(splits[0][1:])
        return (mag, units, measured)
    except Exception as e:
        logging.warn(f'raw: {raw_mag}, e: {e}')
        return (None, None, None)

def lsr_time_to_epoch(time, code):
    text = f'{time} {ingest.code_to_offset(code)}'
    dt = datetime.strptime(text, '%m/%d/%Y %I%M %p %z')
    return int(dt.timestamp()) * 1000

def parse_first_line(line):
    hazard = line[12:29].strip()
    time = line[:12].strip()
    location = line[29:53].strip()
    lat_lon = line[53:67].strip().split(' ')
    lat_lon = [x for x in lat_lon if x.strip()]
    coords = (float(lat_lon[1].replace('W', '')) * -1, float(lat_lon[0][:5]))
    return {'hazard': hazard, 'time': time, 'location': location, 'coords': coords}

def parse_second_line(line, is_tornado):
    date = line[:12].strip()
    if is_tornado:
        # Some WFOs have "UF0" for a tornado mag which breaks parsing
        mag, units, measured = (None, None, None)
    else:
        mag, units, measured = get_mag(line[12:28])
    county = line[28:47].strip()
    state = line[47:53].strip()
    source = line[53:].strip()
    return {'date': date, 'mag': mag, 'units': units, 'measured': measured, 'county': county, 'state': state, 'source': source}

def parse_remarks(lines):
    return ' '.join([line.strip() for line in lines])

def process_filename(filename):
    try:
        events = []
        url = f'{LSR_URL}/{filename}'
        resp = client.get(url)
        lines = [line for line in resp.text.split('\n') if line.strip()]
        in_body = False
        first_line = None
        second_line = None
        remark_lines = []
        tz_code = lines[5].split(' ')[2]

        for line in lines:
            if '..REMARKS..' in line:
                in_body = True
                continue
            if in_body:
                if '&&' in line:
                    in_body = False
                    parsed_first_line = parse_first_line(first_line)
                    hazard = parsed_first_line['hazard']

                    if hazard in TRACKED_HAZARDS:
                        is_tornado = hazard == 'TORNADO'
                        parsed_second_line = parse_second_line(second_line, is_tornado)
                        time = f'{parsed_second_line["date"]} {parsed_first_line["time"]}'
                        report_ts = lsr_time_to_epoch(time, tz_code)
                        ts = ingest.get_ts_from_bulletin(lines[5].strip())
                        delta_minutes = int((ts - report_ts) / 60)
                        if delta_minutes > MINUTES_THRESHOLD:
                            continue
                        report = {
                            'hazard': hazard,
                            'source': parsed_second_line['source'],
                            'mag': parsed_second_line['mag'],
                            'measured': parsed_second_line['measured'],
                            'ts': report_ts,
                            'units': parsed_second_line['units'],
                        }
                        point = parsed_first_line['coords']
                        nearest = ingest.get_nearest(point, cities_tree, cities)
                        event = {
                            'geo': {
                                'point': point,
                                'city': nearest[0],
                                'st': nearest[1],
                                'distance': nearest[2],
                                'bearing': nearest[4]
                            },
                            'report': report,
                            'ts': ts,
                            'type': 'lsr',
                            'url': url,
                        }
                        events.append(event)
                    first_line = None
                    second_line = None
                    remark_lines = []
                elif not first_line:
                    first_line = line
                elif not second_line:
                    second_line = line
                else:
                    remark_lines.append(line)
    except Exception as e:
        print(e)
        logging.warning(traceback.format_exc())
        return None
    return events

def get_new_filenames(last_seen):
    try:
        resp = client.get(f'{LSR_URL}/ls-lt')
        lines = resp.text.split('\n')
        lines.reverse()
        lines = [line for line in lines if line.strip()]
        latest = lines[-1].split(' ')[-1]

        # Stop processing if already up to date
        if last_seen == latest:
            return (latest, [])

        # If a fresh load, wait for new LSRs to process
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
        logging.warn(traceback.format_exc())
        return (last_seen, [])

last_seen = sys.argv[1] if len(sys.argv) > 1 else None
while (True):
    last_seen, filenames = get_new_filenames(last_seen)
    if filenames:
        logging.info(f'Found {len(filenames)} new files')
    events = [process_filename(x) for x in filenames]
    # Flatten list of lists
    events = [item for sublist in events for item in sublist]
    ingest.publish_events(events)
    time.sleep(60)
