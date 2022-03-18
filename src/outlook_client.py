from datetime import datetime
import httpx, os, utils

BASE_URL = 'https://www.spc.noaa.gov/products/outlook/archive'

def get_path(dt, hour):
    date = dt.strftime('%Y%m%d')
    filename = f'KWNSPTSDY1_{date}{hour}.txt'
    return f'data/outlooks/{filename}'

def fetch_outlook(dt, hour):
    year = dt.strftime('%Y')
    date = dt.strftime('%Y%m%d')
    filename = f'KWNSPTSDY1_{date}{hour}.txt'
    url = f'{BASE_URL}/{year}/{filename}'
    print(f'Fetching {url}')
    resp = httpx.get(url)
    if resp.status_code != 200:
        print(f'WARN: Unable to fetch {url}, status code: {resp.status_code}')
        return None
    path = get_path(dt, hour)
    print(f'Saving {path}')
    with open(path, 'w') as file:
        file.write(resp.text)

def get_outlook_lines(dt, hour):
    path = get_path(dt, hour)
    if os.path.isfile(path):
        print(f'Using cached {path}')
    else:
        fetch_outlook(dt, hour)
    with open(path, 'r') as file:
        return file.readlines()


def parse_coords(line_pair):
    lat = line_pair[:4]
    lat = float(lat) / 100
    lon = line_pair[4:]
    lon = f'1{lon}' if lon[0] == '0' else lon
    lon = float(lon) / -100
    return (lon, lat)

def get_tornado_risks(date, hour):
    if not date:
        dt = utils.get_utc_now()
    else:
        dt = datetime.fromisoformat(date)
    outlook_lines = get_outlook_lines(dt, hour)
    in_tornado_section = False
    risks = {}
    risk = None

    for line in outlook_lines:
        line = line.replace('\n', '')
        if not line:
            continue
        if line == '... TORNADO ...':
            in_tornado_section = True
            continue
        if not in_tornado_section:
            continue
        if line == '&&':
            print('Done processing tornado section')
            break
        if line[:4].strip():
            risk = line[:4]
            risks[risk] = []
            line_pairs = line[7:].split(' ')
            parsed_coords = [parse_coords(x) for x in line_pairs]
            risks[risk] += parsed_coords
        else:
            line_pairs = line[7:].split(' ')
            parsed_coords = [parse_coords(x) for x in line_pairs]
            risks[risk] += parsed_coords

    return risks
