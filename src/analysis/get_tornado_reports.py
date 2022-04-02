import httpx, os, pickle
from datetime import datetime
from zoneinfo import ZoneInfo

# https://www.spc.noaa.gov/wcm/index.html#data
URL = 'https://www.spc.noaa.gov/wcm/data/1950-2020_actual_tornadoes.csv'
PATH = 'data/tornado-reports.csv'
START_YEAR = 2014
END_YEAR = 2020

reports = []

def fetch_tornado_reports():
    if os.path.isfile(PATH):
        print(f'Using cached {PATH}')
        return
    print(f'Fetchng {PATH}')
    with open(PATH, 'w') as file:
        with httpx.stream('GET', URL) as r:
            for data in r.iter_text():
                file.writelines(data)

def populate_reports():
    with open(PATH, 'r') as file:
        file.readline()     # Ignore header
        for line in file:
            raw_report = line.strip().split(',')
            # https://www.spc.noaa.gov/wcm/data/SPC_severe_database_description.pdf
            # om, year, month, day, date, time, tz, state, state fips, state number, ef scale, 
            # injuries, fatalities, loss, crop loss, slat, slon, elat, elon, length, width
            year = int(raw_report[1])
            if START_YEAR <= year <= END_YEAR:
                dt = cst_to_utc(f'{raw_report[4]} {raw_report[5]}')
                rating = int(raw_report[10])
                # Unknown f-scale will be -9
                rating = 0 if rating < 0 else rating

                reports.append({
                    'dt': dt,
                    'date': dt.strftime('%Y%m%d'),
                    'state': raw_report[7],
                    'rating': rating,
                    'start': (float(raw_report[16]), float(raw_report[15])),
                    'end': (float(raw_report[18]), float(raw_report[17])),
                    'length': float(raw_report[19]),
                    'width': float(raw_report[20]),
                })

def cst_to_utc(cst):
    dt = datetime.strptime(cst, '%Y-%m-%d %H:%M:%S')
    dt.replace(tzinfo=ZoneInfo('America/Chicago'))
    return dt.astimezone(ZoneInfo("UTC"))

fetch_tornado_reports()
populate_reports()
print(f'Found {len(reports)} reports')
with open('tornado_reports.pkl', 'wb') as file:
    pickle.dump(reports, file)
