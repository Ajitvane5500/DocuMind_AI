# API / Module Documentation

The application currently runs locally through Streamlit and does not provide public HTTP API endpoints.

## PDF processing module (`src.pdf_engine`)

### `extract_pdf(pdf_bytes)`
Input: PDF file bytes.  
Output: list of dictionaries containing `page` (1-based page number) and `text`.

### `make_chunks(pages, chunk_words=180, overlap=35)`
Input: page dictionaries from `extract_pdf`.  
Output: overlapping text chunks with their original page number.

### `retrieve(question, chunks, top_k=3)`
Input: a plain-English question and chunks.  
Output: highest-ranked matching chunks, each with `page`, `text`, and `score`.

### `summarize(text, max_sentences=7)`
Input: extracted document text.  
Output: extractive summary string.

### `make_flashcards(text, count=8)`
Input: extracted document text.  
Output: list of dictionaries with `question` and `answer`.

### `answer_from_chunks(question, matches)`
Input: question and retrieved passages.  
Output: a formatted answer containing the source passages and page numbers.
