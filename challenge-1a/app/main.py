import pdfplumber
import json
import os
from utils import cluster_font_sizes, assign_heading_levels, generate_outline

def extract_elements_from_pdf(pdf_path):
    elements = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            for char in page.chars:
                text = char["text"].strip()
                if text and not text.isspace():
                    elements.append({
                        "text": text,
                        "font_size": float(char["size"]),
                        "page": page_num
                    })
    return elements

def group_by_line(elements, tolerance=0.5):
    from collections import defaultdict
    lines_by_page = defaultdict(list)
    for el in elements:
        page = el["page"]
        y0 = el.get("top", 0)
        matched = False
        for line in lines_by_page[page]:
            if abs(line["y0"] - y0) < tolerance:
                line["texts"].append(el["text"])
                matched = True
                break
        if not matched:
            lines_by_page[page].append({"y0": y0, "texts": [el["text"]], "font_size": el["font_size"], "page": el["page"]})

    final_lines = []
    for lines in lines_by_page.values():
        for line in lines:
            final_lines.append({
                "text": " ".join(line["texts"]),
                "font_size": line["font_size"],
                "page": line["page"]
            })
    return final_lines

if __name__ == "__main__":
    input_pdf = "input.pdf"
    output_json = "outline.json"

    elements = extract_elements_from_pdf(input_pdf)
    lines = group_by_line(elements)
    clustered, kmeans = cluster_font_sizes(lines)
    labeled = assign_heading_levels(clustered, kmeans)
    outline = generate_outline(labeled)

    with open(output_json, "w") as f:
        json.dump(outline, f, indent=2)

    print(f"\n✅ Outline saved to {output_json}")
