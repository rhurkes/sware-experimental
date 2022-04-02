import httpx, ingest, logging, re, sys, time, traceback
from datetime import datetime

MD_URL = 'https://www.spc.noaa.gov/products/md'

logging.basicConfig(filename='wx-md.log', encoding='utf-8', level=logging.INFO)
client = httpx.Client(timeout=10.0)

def process_md(md, year):
    event = None
    try:
        url = f'{MD_URL}/{year}/md{md}.txt'
        resp = client.get(url)
        lines = resp.text.split('\n')
        date = lines[7]
        date = date.split(' ')
        date = f'{date[6]}-{date[4]}-{date[5]} {date[0]} {date[1]} {ingest.code_to_offset(date[2])}'
        ts = int(datetime.strptime(date, '%Y-%b-%d %I%M %p %z').timestamp()) * 1000
        new_lines = []
        for line in lines[9:15]:
            value = line.strip() if line.strip() else '|'
            new_lines.append(value)
        new_lines = ' '.join(new_lines)
        new_lines = new_lines.split('|')
        new_lines = [x.strip() for x in new_lines if x.strip()]
        area = new_lines[0].replace('Areas affected...', '')
        subject = new_lines[1].replace('Concerning...', '')
        if subject[-3:] == '...':
            subject = subject[:-3]
        event = {
            'img_url': f'{MD_URL}/{year}/mcd{md}.gif',
            'source_id': md,
            'subject': subject,
            'subject2': area,
            'ts': ts,
            'type': 'md',
            'source': 'spc',
            'url': url
        }
    except:
        logging.warning(traceback.format_exc())
    return event

def get_new_filenames(last_seen, year):
    new_mds = []
    new_last_seen = last_seen

    try:
        resp = client.get(f'{MD_URL}/{year}/')
        matches = re.findall(r"\"md(\d{4}).txt\"", resp.text)
        new_last_seen = matches[-1]
        if last_seen is None:
            return (new_last_seen, new_mds)
        new_mds = []
        reached_lastseen = False
        for match in matches:
            if match == last_seen:
                reached_lastseen = True
                continue
            if reached_lastseen:
                new_mds.append(match)
    except Exception as e:
        logging.warning(traceback.format_exc())
    return (new_last_seen, new_mds)

last_seen = sys.argv[1] if len(sys.argv) > 1 else None
while (True):
    year = datetime.utcnow().year
    last_seen, mds = get_new_filenames(last_seen, year)
    if mds:
        logging.info(f'Found new MDs: {mds}')
    events = [process_md(md, year) for md in mds]
    ingest.publish_events(events)
    time.sleep(60)
