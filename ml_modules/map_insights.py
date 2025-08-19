import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

def extract_lat_lon(listings):
    locs = []
    for l in listings:
        loc_str = l.get('location', None)
        if loc_str and ',' in loc_str:
            try:
                lat, lon = map(float, loc_str.split(','))
                locs.append([lat, lon])
            except Exception:
                continue
    return np.array(locs) if locs else np.array([])

def compute_clusters(listings, n_clusters=5):
    locs = extract_lat_lon(listings)
    if len(locs) < n_clusters:
        n_clusters = max(1, len(locs))
    if len(locs) < 2:
        return [], []
    kmeans = KMeans(n_clusters=min(n_clusters, len(locs)), random_state=42, n_init='auto')
    labels = kmeans.fit_predict(locs)
    centers = kmeans.cluster_centers_
    return labels, centers
