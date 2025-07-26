<<<<<<< HEAD
# Adobe-India-Hackathon25
=======

# Adobe India Hackathon 2025 – Challenge 1A: PDF Outline Extractor

## Overview

This repository contains a fully offline, Dockerized solution for **Challenge 1A** of the Adobe India Hackathon 2025. The task is to **extract a structured outline** (including Title, H1, H2, H3 headings with their page numbers) from PDFs and output results in JSON format. The solution adheres strictly to performance, architecture, and resource constraints provided by Adobe.

---

## Key Highlights

-  Uses `pdfplumber` for precise text extraction from PDFs
-  Uses `scikit-learn`'s KMeans for font-size-based heading clustering
-  Generates structured JSON outlines including `Title`, `H1`, `H2`, `H3`
-  Executes under 10 seconds for 50-page PDFs (within 16 GB RAM)
-  Fully containerized, CPU-only, works on AMD64 architecture
-  100% offline — no internet access required at runtime

---

##  Project Structure

```
Challenge_1a/
├── app/
│   ├── main.py            # Main script to process all PDFs in input/
│   ├── utils.py           # Heading extraction and clustering logic
├── sample_dataset/
│   ├── pdfs/              # Input PDFs (read-only)
│   ├── outputs/           # Output JSON files
│   └── schema/
│       └── output_schema.json  # JSON schema specification
├── Dockerfile             # Container definition
├── requirements.txt       # Python dependencies
├── README.md              # This file
```

---

##  Input & Output

| Parameter         | Description                           |
|------------------|---------------------------------------|
| Input Path       | `/app/input` (read-only volume)       |
| Output Path      | `/app/output` (write volume)          |
| Output Format    | One JSON file per input PDF           |
| Output Naming    | `filename.pdf` → `filename.json`      |
| Schema Compliance| Matches `/schema/output_schema.json`  |

---

##  Build & Run Instructions

###  Build the Docker image (AMD64, no internet)
```bash
docker build -t pdf-outline .
```

### ▶ Run inference on mounted input/output directories
```bash
docker run --rm -v "${PWD}:/app" -w /app pdf-outline python app/main.py
```
>  All JSON files will be saved in `sample_dataset/outputs/`.

---

##  Tech Stack

- **Language**: Python 3.10
- **PDF Parsing**: [`pdfplumber`](https://github.com/jsvine/pdfplumber)
- **Clustering**: [`scikit-learn`](https://scikit-learn.org)
- **Data Handling**: `numpy`, `json`
- **Containerization**: Docker (Linux, AMD64)

---

##  Adobe Challenge Compliance Checklist

| Constraint                        | Status |
|----------------------------------|--------|
| ≤ 10 seconds per 50-page PDF     | ✅     |
| No internet access at runtime    | ✅     |
| Works on AMD64 CPU               | ✅     |
| ≤ 200MB ML model size            | ✅     |
| All PDFs auto-processed          | ✅     |
| Output conforms to schema        | ✅     |
| Read-only access to input        | ✅     |

---

##  Sample Output Schema

Each output file includes:
```json
{
  "Title": "Document Title",
  "Headings": [
    { "text": "Heading A", "level": "H1", "page": 1 },
    { "text": "Subheading A.1", "level": "H2", "page": 1 },
    { "text": "Sub-subheading A.1.1", "level": "H3", "page": 2 }
  ]
}
```

---

## Author

**Arsh Verma & Prakhar Khare **
---
>>>>>>> eafdd85 (FINAL COMMIT : challange 1a completed)
