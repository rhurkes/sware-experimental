from datetime import datetime
import httpx, ingest, logging, sys, time, traceback

BASE_URL = 'https://tgftp.nws.noaa.gov/SL.us008001/DF.c5/DC.textf/DS.selww'

logging.basicConfig(filename='wx-sel.log', encoding='utf-8', level=logging.INFO)
client = httpx.Client(timeout=10.0)

def process_file(filename):
    print(filename)
    event = None
    try:
        url = f'{BASE_URL}/{filename}'
        resp = client.get(url)
        text = resp.text.replace('\r', '')
        if 'HAS CANCELLED' in text:
            return event
        pds = 'THIS IS A PARTICULARLY DANGEROUS SITUATION' in text
        lines = text.split('\n')
        area = None
        for line in lines:
            if len(line) and line[0] == '*':
                if area is not None:
                    break
                else:
                    area = line.strip()
            elif area is not None:
                area += f'{line},'
        while '  ' in area:
            area = area.replace('  ', ' ')
        while area[-1] == ',':
            area = area[:-1]
        area = area.replace('* Tornado Watch ', '')
        area = area.replace('* Severe Thunderstorm Watch ', '')
        watch_id = lines[7].split(' ')[-1]
        if len(watch_id) == 2:
            watch_id = f'00{watch_id}'
        elif len(watch_id) == 3:
            watch_id = f'0{watch_id}'
        event = {
            'img_url': f'https://www.spc.noaa.gov/products/watch/{datetime.now().year}/ww{watch_id}_radar_init.gif',
            'pds': pds,
            'subject': f'{lines[7]} {area}',
            'ts': ingest.get_ts_from_bulletin(lines[9]),
            'type': 'sel',
            'url': url,
        }
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
