import httpx, ingest, logging, sys, time, traceback

BASE_URL = 'https://tgftp.nws.noaa.gov/SL.us008001/DF.c5/DC.textf/DS.swoac'

logging.basicConfig(filename='wx-swo.log', encoding='utf-8', level=logging.INFO)
client = httpx.Client(timeout=10.0)

def process_file(filename):
    event = None
    try:
        url = f'{BASE_URL}/{filename}'
        resp = client.get(url)
        text = resp.text.replace('\r', '')
        lines = text.split('\n')
        if 'ACUS01' not in lines[1]:
            return None
        risk = ''
        risk_block = lines[11:]
        for line in risk_block:
            if not line.strip():
                break
            risk += f' {line}'
        risk = risk[4:]
        while risk[-1] == '.':
            risk = risk[:-1]
        event = {
            'img_url': 'https://www.spc.noaa.gov/products/outlook/day1otlk.gif',
            'subject': risk,
            'ts': ingest.get_ts_from_bulletin(lines[7]),
            'type': 'swo',
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
        logging.info(f'Found new files: {filenames}')
    events = [process_file(x) for x in filenames]
    ingest.publish_events(events)
    time.sleep(60)
