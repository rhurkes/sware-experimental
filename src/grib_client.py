import matplotlib.pyplot as plt
import pygrib
import json

# SOURCES
# Only has last 48 hours
# https://nomads.ncep.noaa.gov/pub/data/nccf/com/hrrr/prod/hrrr.20220313/conus/
# Pressure sfc are 300-700mb
# Sfc are ~150mb

# https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrr_download.cgi
# Thank you for visiting this resource. With the expanded availability of archived HRRR grib2-formatted data now courtesy of NOAA and the Registry of Open Data on AWS, this archive hosted at the University of Utah is now being reduced. Users interested in the grib2 format are encouraged to switch to using the AWS archive, or a similar archive operated within the Google Cloud.

# https://www.cpc.ncep.noaa.gov/products/wesley/fast_downloading_grib.html

# https://registry.opendata.aws/noaa-hrrr-pds/
# https://noaa-hrrr-bdp-pds.s3.amazonaws.com/hrrr.20220305/conus/hrrr.t12z.wrfsfcf00.grib2

# Inventory: https://www.nco.ncep.noaa.gov/pmb/products/hrrr/hrrr.t00z.wrfsfcf00.grib2.shtml
    # Also can print for grb in grbs

# https://nomads.ncep.noaa.gov/
    # Filters make it way smaller: http://davidburchnavigation.blogspot.com/2019/06/how-to-request-grib-files-by-parameter.html

# https://jswhit.github.io/pygrib/api.html#example-usage

# STRATEGY
# Based of 7-11: storms have to be after 11am
    # TODO how does this work with CO setup
# Don't go past Sunset, or maybe 10pm?
# TODO what's in IDX files?

BASE_HOUR = 12
UPDRAFT_HELICITY_THRESHOLD = 75

def in_bounds(lon, lat):
    return lon > -103 and lon < 97 and lat > 32 and lat < 40

def get_hour(forecast_hour):
    hour = BASE_HOUR + int(forecast_hour)
    return hour - 24 if hour >= 24 else hour

def in_bounds(lon, lat):
    return lon > -103 and lon < 97 and lat > 32 and lat < 40

def add_grib_features(forecast_hour, output):
    print(f'Processing grib {forecast_hour}')
    # create grib message iterator
    grbs = pygrib.open(f'/home/rob/Downloads/hrrr.t{BASE_HOUR}z.wrfsfcf{forecast_hour}(1).grib2')
    grbs.seek(0)

    # get 2km-5km max updraft helicity message. 2d grid with (1059, 1799) shape.
    grb = grbs.select(stepType='max', parameterUnits='199', level=5000)[0]
    values = grb.values

    # get lats, lons
    lats, lons = grb.latlons()

    # naive wrangling of features, TODO is there a better way of doing this?
    for row, row_values in enumerate(values):
        for col, value in enumerate(row_values):
            if value >= UPDRAFT_HELICITY_THRESHOLD:
                # TODO take bounds from elsewhere
                if in_bounds(lons[row][col], lats[row][col]):
                    output['features'].append((lons[row][col], lats[row][col]))
                    output['metadata'].append((int(value), get_hour(forecast_hour)))

output = {'features': [], 'metadata': []}
for i in range(5, 13):
    hour = f'0{i}' if i < 10 else str(i)
    add_grib_features(hour, output)

serialized = json.dumps(output)
with open('grib_test.json', 'w') as file:
    file.write(serialized)
