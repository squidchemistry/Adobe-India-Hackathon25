import numpy as np
from sklearn.cluster import KMeans

def cluster_font_sizes(elements, n_clusters=3):
    if len(elements) < n_clusters:
        n_clusters = len(elements)  # Avoid KMeans error when too few samples

    if n_clusters == 0:
        raise ValueError("No elements found to cluster.")

    font_sizes = np.array([[el["font_size"]] for el in elements])
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(font_sizes)

    for i, el in enumerate(elements):
        el["cluster"] = kmeans.labels_[i]
    return elements, kmeans

    font_sizes = np.array([[el["font_size"]] for el in elements])
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(font_sizes)
    for i, el in enumerate(elements):
        el["cluster"] = kmeans.labels_[i]
    return elements, kmeans

def assign_heading_levels(elements, kmeans):
    centers = kmeans.cluster_centers_.flatten()
    sorted_clusters = sorted(range(len(centers)), key=lambda i: -centers[i])
    cluster_to_level = {sorted_clusters[i]: f"H{i+1}" for i in range(len(sorted_clusters))}
    for el in elements:
        el["level"] = cluster_to_level[el["cluster"]]
    return elements

def generate_outline(elements):
    outline = {"Title": None, "Headings": []}
    for el in elements:
        entry = {"text": el["text"], "level": el["level"], "page": el["page"]}
        if el["level"] == "H1" and not outline["Title"]:
            outline["Title"] = el["text"]
        else:
            outline["Headings"].append(entry)
    return outline
