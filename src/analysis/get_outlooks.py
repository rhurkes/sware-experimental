import httpx, os, pickle, time
from datetime import datetime, timedelta

BASE_URL = 'https://www.spc.noaa.gov/wcm/data/1950-2020_actual_tornadoes.csv'
PATH = 'data/tornado-reports.csv'
START_YEAR = 2014
END_YEAR = 2020

client = httpx.Client()

def fetch_outlooks():
    dt = datetime(START_YEAR, 1, 1)
    while dt.year <= END_YEAR:
        date = dt.strftime('%Y%m%d')
        image_file = f'day1probotlk_{date}_1300_torn_prt.gif'
        image_url = f'https://www.spc.noaa.gov/products/outlook/archive/{dt.year}/{image_file}'
        image_path = f'data/outlook-images/{image_file}'
        if not os.path.isfile(image_path):
            time.sleep(0.1)
            resp = client.get(image_url)
            with open(image_path, 'wb') as file:
                file.write(resp.content)
        outlook_file = f'KWNSPTSDY1_{date}1300.txt'
        outlook_url = f'https://www.spc.noaa.gov/products/outlook/archive/{dt.year}/{outlook_file}'
        outlook_path = f'data/outlooks/{outlook_file}'
        if not os.path.isfile(outlook_path):
            time.sleep(0.1)
            resp = client.get(outlook_url)
            with open(outlook_path, 'wb') as file:
                file.write(resp.content)
        dt = dt + timedelta(days=1)

def parse_coords(line_pair):
    lat = line_pair[:4]
    lat = float(lat) / 100
    lon = line_pair[4:]
    lon = f'1{lon}' if lon[0] == '0' else lon
    lon = float(lon) / -100
    return (lon, lat)

def get_risks(lines):
    risks = {}
    risk = None
    in_tornado_section = False
    current_polygon = None

    for line in lines:
        line = line.replace('\n', '')
        if not line:
            continue
        if line == '... TORNADO ...':
            in_tornado_section = True
            continue
        if not in_tornado_section:
            continue
        if line == '&&':
            break
        if line[:4].strip():
            risk = line[:4]
            if risk not in risks:
                risks[risk] = [[]]
                current_polygon = risks[risk][0]
            else:
                risks[risk].append([])
                current_polygon = risks[risk][-1]
        line_pairs = line[7:].split(' ')
        parsed_coords = [parse_coords(x) for x in line_pairs]
        current_polygon += (parsed_coords)
    return risks

# date format: 20140521
def parse_outlook(date):
    outlook_file = f'KWNSPTSDY1_{date}1300.txt'
    path = f'data/outlooks/{outlook_file}'
    with open(path, 'r') as file:
        return get_risks(file.readlines())        

def parse_outlooks():
    daily_risks = {}
    dt = datetime(START_YEAR, 1, 1)
    while dt.year <= END_YEAR:
        date = dt.strftime('%Y%m%d')
        daily_risks[date] = parse_outlook(date)
        dt = dt + timedelta(days=1)
    return daily_risks

fetch_outlooks()
outlooks = parse_outlooks()
print(f'Parsed {len(outlooks)} outlooks')
with open('outlooks.pkl', 'wb') as file:
    pickle.dump(outlooks, file)
