# https://realpython.com/k-means-clustering-python/

import json
from pyexpat import features
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from kneed import KneeLocator
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np
from statistics import mean

def do_work():
    with open('grib_test.json', 'r') as file:
        output = json.loads(file.read())

    # standardize the features, ie. the lat/lon pairs
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(output['features'])

    # kmeans_kwargs = {
    #     'init': 'k-means++',
    #     'n_init': 10,
    #     'max_iter': 300,
    #     'random_state': 69,
    # }

    # # a list holds the SSE values for each k
    # sse = []
    # for k in range(1, 11):
    #     kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    #     kmeans.fit(scaled_features)
    #     sse.append(kmeans.inertia_)

    # kl = KneeLocator(
    #     range(1, 11), sse, curve="convex", direction="decreasing"
    # )

    # convex elbow says 3, silhouette says 9, concave elbow 10
    # concave increasing is 1, convex increasing is 10
    # 4 puts 2 of them in a weird spot
    # I really like 5-6 even though those are the lowest silhouette scores
    # n_clusters = kl.elbow
    # print(f'Using {n_clusters} cluster size')


    # kmeans = KMeans(
    #     init='k-means++',
    #     n_clusters=n_clusters,
    #     n_init=10,
    #     max_iter=300,
    # )

    # kmeans.fit(scaled_features)
    # centers = kmeans.cluster_centers_
    # inverse = scaler.inverse_transform(centers)

    # things = []
    # for inv in inverse:
    #     things.append((inv[0], inv[1]))
    # return things


    # https://stackoverflow.com/questions/34579213/dbscan-for-clustering-of-geographic-location-data
    # eps 0.3 gives 6 clusters, 0.2 gives 10 clusters, 0.4 gives 5 clusters, 0.5 gives 4 clusters, 0.6 gives 3 clusters
    dbscan = DBSCAN(eps=0.4)
    dbscan.fit(scaled_features)
    clusters = {}
    for i, id in enumerate(dbscan.labels_):
        if id == -1:
            continue
        key = str(id)
        if key not in clusters:
            clusters[key] = {'features': [], 'metadata': []}
        clusters[key]['features'].append(output['features'][i])
        clusters[key]['metadata'].append(output['metadata'][i])
    print(f'Found {len(clusters)} clusters')

    # For each cluster, decorate with initiation details
    for cluster_id in clusters:
        cluster = clusters[cluster_id]
        # Features are added as the grib is iterated through, so use hour from the first feature
        init_hour = cluster['metadata'][0][1]
        cluster['init_hour'] = init_hour
        lons = []
        lats = []
        # TODO this is broken
        # TODO iterate through features checking each one's metadata
        for i, value in enumerate(cluster['features']):
            if cluster['metadata'][i][1] == init_hour:
                lons.append(cluster['features'][i][0])
                lats.append(cluster['features'][i][1])
        cluster['init_coord'] = (mean(lons), mean(lats))
    with open('clusters.json', 'w') as file:
        file.write(json.dumps(clusters))
    return clusters