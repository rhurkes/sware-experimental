import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader
from shapely.geometry.polygon import Polygon
import json, statistics, pickle
from pyexpat import features
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from kneed import KneeLocator
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np
from statistics import mean

WEST_BOUND = -107.2 # Rawlin, WY
EAST_BOUND = -84.2  # Tallahassee, FL
BOUNDS = [EAST_BOUND, WEST_BOUND, 25, 50]

plt.figure(figsize = (16,20), dpi = 100)    
ax = plt.axes(projection=ccrs.LambertConformal())
ax.set_extent(BOUNDS)

# Draw states
shapename = 'admin_1_states_provinces_lakes_shp'
states_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)
for state in shpreader.Reader(states_shp).geometries():
    facecolor = 'white'
    edgecolor = 'black'
    ax.add_geometries([state], ccrs.PlateCarree(), facecolor=facecolor, edgecolor=edgecolor)

# Draw reports
# List of all reports in format: dt, state, rating, start, end, length, width
with open('tornado_reports.pkl', 'rb') as file:
    reports = pickle.load(file)

features = []
for report in reports:
    lon = report['start'][0]
    lat = report['start'][1]
    if BOUNDS[1] <= lon <= BOUNDS[0] and BOUNDS[2] <= lat <= BOUNDS[3]:
        features.append([report['start'][0], report['start'][1]])

# Get clusters - DBScan works really poorly for this, so use kmeans
# standardize the features, ie. the lat/lon pairs
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

kmeans_kwargs = {
    'init': 'k-means++',
    'n_init': 10,
    'max_iter': 300,
    'random_state': 69,
}

# a list holds the SSE values for each k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_features)
    sse.append(kmeans.inertia_)
kl = KneeLocator(range(1, 11), sse, curve="convex", direction="decreasing")
n_clusters = kl.elbow
n_clusters = 6  # Override with manual cluster size

kmeans = KMeans(
    init='k-means++',
    n_clusters=n_clusters,
    n_init=10,
    max_iter=300,
)

kmeans.fit(scaled_features)
clusters = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
colors = {0: 'red', 1: 'blue', 2: 'green', 3: 'magenta', 4: 'brown', 5: 'pink', 6: 'purple', 7: 'orange', 8: 'olive', 9: 'cyan'}
for i, label in enumerate(kmeans.labels_):
    if label == -1:
        continue
    clusters[label].append(features[i])

# Draw clustered reports
for key in clusters:
    color = colors[key]
    for report in clusters[key]:
        ax.plot(report[0], report[1], '.', color=color, transform=ccrs.PlateCarree(), markersize=2)

# Draw cluster centroids
centers = scaler.inverse_transform(kmeans.cluster_centers_)
for center in centers:
    ax.plot(center[0], center[1], 'o', color='black', transform=ccrs.PlateCarree(), markersize=20)

plt.savefig('report_clustering.png')
