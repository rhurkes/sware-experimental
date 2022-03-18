# sware
Situational Awareness for Severe Weather

# Outlook Client
This script returns SPC outlook tornado probabilities for a given date and time. If the outlook is not on the local file system, it will be downloaded and stored.

# HRRR Client
https://www.nco.ncep.noaa.gov/pmb/products/hrrr/


# Local Development
- `python3 -m venv venv`
- `pip3 install -r requirements.txt`
- direct deps: matplotlib, httpx, cartopy, pygrib, sklearn, kneed (only if using kmeans/elbow)

# Model decisions

# Model TODOs
- How should I use risk areas? Do I use 2% for bounds?
- Do I only incude updraft helicities within bounds of whatever risk I go with?

# TODO
- Discord bot

