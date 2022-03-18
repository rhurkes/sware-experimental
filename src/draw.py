import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader
import json
import model
import statistics
import outlook_client
import outlook_analysis
from shapely.geometry.polygon import Polygon

def get_max_updraft_helicity_color(value):
    if value < 75:
        return '#0081FF'
    if value < 100:
        return '#00B9FF'
    if value < 125:
        return '#00EAFF'
    if value < 150:
        return '#71E300'
    if value < 175:
        return '#B8FF3A'
    if value < 200:
        return '#FFEC00'
    if value < 225:
        return '#FFBB03'
    if value < 250:
        return '#FF6B05'
    if value < 275:
        return '#FF2C00'
    if value < 300:
        return '#FF00E3'
    else:
        return '#F4B7F5'

# Get bounds
risks = outlook_client.get_tornado_risks('2017-05-16', '1300')
bounds = outlook_analysis.get_padded_bounds(risks['0.05'], 0.5)

plt.figure(figsize = (16,20), dpi = 100)    
ax = plt.axes(projection=ccrs.LambertConformal())
ax.set_extent([bounds['min_lon'], bounds['max_lon'], bounds['min_lat'], bounds['max_lat']])

# Draw states
shapename = 'admin_1_states_provinces_lakes_shp'
states_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)

for state in shpreader.Reader(states_shp).geometries():
    facecolor = 'white'
    edgecolor = 'black'
    ax.add_geometries([state], ccrs.PlateCarree(), facecolor=facecolor, edgecolor=edgecolor)

# TODO real colors
# Draw risks
risk_colors = {'0.05': (0.5, 0, 0, 0.1), '0.10': 'orange', '0.15': 'red'}
for risk in risks:
    # Ignore 2%
    if risk == '0.02':
        continue
    if risk == 'SIGN':
        # TODO
        continue
    polygon = Polygon(risks[risk])
    ax.add_geometries([polygon], ccrs.PlateCarree(), facecolor=risk_colors[risk], edgecolor='black')

# TODO it'd be nice to not have to transform everything
with open('grib_test.json', 'r') as file:
    features = json.loads(file.read())

for feature in features:
    lon = feature[0]
    lat = feature[1]
    # value = feature[2]
    # color = get_max_updraft_helicity_color(value)
    color = 'black'
    # https://matplotlib.org/2.1.2/api/_as_gen/matplotlib.pyplot.plot.html
    ax.plot(lon, lat, '.', color=color, transform=ccrs.PlateCarree(), markersize=2)

color = {'0': 'black', '1': 'red', '2': 'blue', '3': 'brown', '4': 'green', '5': 'purple', '6': 'orange', '7': 'grey', '8': 'yellow', '9': 'red', '10': 'blue', '11': 'green'}

# Testing output of model.py
clusters = model.do_work()
for key in clusters:
    cluster = clusters[key]
    c = color[key]
    # Plot actual data
    for thing in cluster['features']:
        ax.plot(thing[0], thing[1], '.', color=c, transform=ccrs.PlateCarree(), markersize=2)
    # Plot cluster means
    # mean_lon = statistics.mean([x[0] for x in cluster['features']])
    # mean_lat = statistics.mean([x[1] for x in cluster['features']])
    # ax.plot(mean_lon, mean_lat, 'x', color=c, transform=ccrs.PlateCarree(), markersize=30)
    # Plot initial mean coord
    ax.plot(cluster['init_coord'][0], cluster['init_coord'][1], 'x', color=c, transform=ccrs.PlateCarree(), markersize=25)

plt.savefig('test.png')
