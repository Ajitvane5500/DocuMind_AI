# DocuMind AI — Intelligent PDF Assistant

DocuMind AI helps students, researchers and professionals work with lengthy PDF documents. Upload a PDF, retrieve relevant passages by asking questions, create a concise executive summary, and generate study flashcards.

## Features
- Upload and extract text from PDF files.
- Split content into page-aware text sections.
- Search relevant sections for natural-language questions using TF-IDF relevance scoring.
- Show source page numbers and retrieved passages to support traceability.
- Generate an extractive executive summary.
- Generate simple study flashcards from definition-style and informative sentences.

## Technology stack
- **Python** — application logic
- **Streamlit** — interactive web interface
- **PyMuPDF** — PDF text extraction
- **scikit-learn** — TF-IDF vectorization and cosine-similarity retrieval

> Note: This starter version provides relevance-based retrieval, not a generative LLM. It returns source passages instead of making up answers. Scanned/image-only PDFs require OCR and are not supported in this version.

## Run locally
1. Install Python 3.10 or later.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```
6. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Deploy on Streamlit Community Cloud
1. Push this repository to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Select **Create app** and choose this GitHub repository.
4. Set the main file path to `app.py`.
5. Deploy.

## API / module documentation
This project is a self-contained web app and does not expose a network REST API.

| Function | Purpose |
|---|---|
| `extract_pdf(pdf_bytes)` | Extracts text from each PDF page. |
| `make_chunks(pages, chunk_words=180, overlap=35)` | Creates overlapping text chunks while preserving page numbers. |
| `retrieve(question, chunks, top_k=3)` | Ranks document chunks using TF-IDF and cosine similarity. |
| `summarize(text, max_sentences=7)` | Builds an extractive summary from informative sentences. |
| `make_flashcards(text, count=8)` | Creates question/answer study cards from document sentences. |
| `answer_from_chunks(question, matches)` | Formats retrieved passages as a grounded response. |

## Repository structure
```text
DocuMind_AI/
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   └── pdf_engine.py
└── sample_docs/
```

## Limitations and future scope
- OCR support for scanned PDFs.
- True embedding-based semantic search.
- LLM-generated answers and summaries with citations.
- Support for DOCX and PPTX.
- User accounts and document history.

## Responsible use
Check source passages before relying on generated study material. Do not upload confidential or personally sensitive documents to a public deployment.
