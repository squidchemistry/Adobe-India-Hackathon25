import numpy as np                        # used for numerical operations
from sklearn.cluster import KMeans        # to group font sizes into clusters
import streamlit as st                    # using streamlit for UI

def cluster_font_sizes(elements, n_clusters=3):
    if len(elements) < n_clusters:        
        n_clusters = len(elements)  # Avoid KMeans error when too few samples

    if n_clusters == 0:         # if no elements are provided, raise an error
        raise ValueError("No elements found to cluster.")

    font_sizes = np.array([[el["font_size"]] for el in elements]) # cluster based on font sizes
    
    with st.spinner("🔢 Clustering font sizes..."):  # when clustering happens display spinner
        kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(font_sizes)

    for i, el in enumerate(elements):  # to each element provide a  cluster label
        el["cluster"] = int(kmeans.labels_[i])  # cast to int for JSON compatibility
    return elements, kmeans     


def assign_heading_levels(elements, kmeans):
    centers = kmeans.cluster_centers_.flatten()   
    sorted_clusters = sorted(range(len(centers)), key=lambda i: -centers[i])       # clusters sorted by size
    cluster_to_level = {sorted_clusters[i]: f"H{i+1}" for i in range(len(sorted_clusters))}    # assign heading levels based on cluster size

    for el in elements:
        el["level"] = cluster_to_level[el["cluster"]]

    st.success("🏷️ Heading levels assigned")
    return elements


def generate_outline(elements):
    outline = {"Title": None, "Headings": []}   # Generates the outline structure with title and headings
    for el in elements:
        entry = {                               # to create an entry for each element
            "text": el["text"],
            "level": el["level"],
            "page": el["page"]
        }

        if el["level"] == "H1" and not outline["Title"]:     # if it's the first H1, set it as the title
            outline["Title"] = el["text"]
        else:
            outline["Headings"].append(entry)

    st.success("🧾 Outline generated")
    return outline
