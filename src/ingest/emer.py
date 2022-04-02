import httpx

API_URL = 'http://localhost:8080/events'

client = httpx.Client(timeout=10.0)
events = []
events.append({
    'img_url': 'https://www.spc.noaa.gov/products/outlook/archive/2012/day1otlk_20120414_1300_prt.gif',
    'subject': 'THERE IS A HIGH RISK OF SVR TSTMS LATER THIS AFTERNOON INTO TONIGHT FOR CENTRAL/ERN NEB...CENTRAL/ERN KS...AND CENTRAL/N CENTRAL OK',
    'ts': 1648062600000,
    'type': 'swo',
    'url': 'https://www.spc.noaa.gov/exper/archive/event.php?date=20120414',
})
events.append({
    'img_url': 'https://www.spc.noaa.gov/products/watch/2012/ww0165_radar.gif',
    'pds': True,
    'subject': 'THE NWS STORM PREDICTION CENTER HAS ISSUED A TORNADO WATCH FOR PORTIONS OF CENTRAL KANSAS, NORTHWEST OKLAHOMA',
    'ts': 1648062600000,
    'type': 'sel',
    'url': 'https://www.spc.noaa.gov/exper/archive/event.php?date=20120414',
})
events.append({
    'geo': {
        'point': (-98, 37),
        'city': 'Wichita',
        'st': 'KS',
        'distance': 2,
        'bearing': 'SW',
    },
    'emergency': True,
    'subject': 'Stuff',
    'ts': 1648062600000,
    'type': 'tor',
    'url': 'https://www.spc.noaa.gov/exper/archive/event.php?date=20120414',
    'wfo': 'ICT',
})

client.post(API_URL, json=events)
