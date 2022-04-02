# Must Have
[ ] Warning ! Icon when going two minutes without data
[ ] Test polling
[ ] DEPLOY

# Nice to have
[ ] Button to get SPC Mesoanalysis (4h)
    - https://www.spc.noaa.gov/exper/mesoanalysis/new/getclimoenv.php?lat=45.21906415869187&lon=-94.18714102560628&src=1&1648152283769
    - `82 March 24 2022032421,121,46,0.27,0.8,223,52.54,114.81,463.62,31,8.91 23, 14, 7, 3, 2, 0 0.515`
    - Grid point (46, 122), STP 0.3, SCP 0.8, MLCAPE 223, Eff Shear 52, Eff Hel 114, MLLCL 463
[ ] TESTS
[ ] Linting on py and js

# Future
[ ] Publish diagnostic msgs
[ ] Hold onto last outlook, current MDs, current watches? (1h)

# https://forecast.weather.gov/product_types.php?site=NWS
# https://www.weather.gov/documentation/services-web-api
# https://www.weather.gov/tg/dataprod
# https://www.weather.gov/tg/txtfiles
# https://tgftp.nws.noaa.gov/SL.us008001/DF.c5/DC.textf/
# Data Format (ASCII), Data Category, Data Subcategory

# Local testing
- `open -n -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --user-data-dir="/tmp/chrome_dev_test" --disable-web-security`

# Found old shapefile
# Converted to GeoJSON
# http://wiki.gis.com/wiki/index.php/Decimal_degrees (Truncate to 4 places, 11.1m accuracy)