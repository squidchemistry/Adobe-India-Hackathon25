import streamlit as st          #using streamlit for UI
import pdfplumber               #content reading and extracting from PDF files
import json                     # change data extracted to JSON format
from io import BytesIO          # for handling byte streams
from utils import cluster_font_sizes, assign_heading_levels, generate_outline    # import utility functions

# --------------------
# Helper Functions
# --------------------

def extract_elements_from_pdf(file):     # Extract text, font sizes,page and position from PDF
    elements = []
    with pdfplumber.open(file) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            for char in page.chars:
                text = char["text"].strip()
                if text and not text.isspace():
                    elements.append({
                        "text": text,
                        "font_size": float(char["size"]),
                        "page": page_num,
                        "top": float(char["top"])
                    })
    return elements

def group_by_line(elements, tolerance=0.5):      # Group elements by lines based on their vertical position
    from collections import defaultdict
    lines_by_page = defaultdict(list)
    for el in elements:
        page = el["page"]
        y0 = el.get("top", 0)
        matched = False
        for line in lines_by_page[page]:            # group elements by their y-coordinate proximity
            if abs(line["y0"] - y0) < tolerance:
                line["texts"].append(el["text"])
                matched = True
                break
        if not matched:                               # if no existing line matches, create a new one
            lines_by_page[page].append({
                "y0": y0,
                "texts": [el["text"]],
                "font_size": el["font_size"],
                "page": el["page"]
            })

    final_lines = []                          # Collect all grouped lines into a final list
    for lines in lines_by_page.values():
        for line in lines:
            final_lines.append({
                "text": " ".join(line["texts"]),
                "font_size": line["font_size"],
                "page": line["page"]
            })
    return final_lines

# --------------------
# Streamlit App UI
# --------------------

st.set_page_config(page_title="PDF Outline Extractor", layout="centered")
st.title("📄 PDF Outline Extractor") 

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])    # Uploader for PDF files

if uploaded_file:           
    with st.spinner("🔍 Processing PDF..."):
        elements = extract_elements_from_pdf(uploaded_file)         # to extract text, font sizes, page numbers and positions from PDF
        lines = group_by_line(elements)                             
        clustered, kmeans = cluster_font_sizes(lines)               
        labeled = assign_heading_levels(clustered, kmeans)          
        outline = generate_outline(labeled)                         

    st.success("✅ Outline Extracted!")

    st.subheader("📋 Extracted Outline (JSON)")                    
    st.json(outline)

    # Download Button
    json_bytes = json.dumps(outline, indent=2).encode("utf-8")      
    st.download_button("⬇️ Download Outline JSON", json_bytes, "outline.json", "application/json")
