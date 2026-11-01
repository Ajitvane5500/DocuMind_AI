import re
from collections import Counter
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOP = set("""a an the and or but if then of in on at to for from by with is are was were be been being this that these those it its as into about than can could should would may might will shall we you they them their our your i he she his her not no do does did have has had""".split())

def extract_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for idx, page in enumerate(doc, start=1):
        pages.append({"page": idx, "text": page.get_text("text").strip()})
    return pages

def make_chunks(pages, chunk_words=180, overlap=35):
    chunks = []
    for page in pages:
        words = page["text"].split()
        start = 0
        while start < len(words):
            part = " ".join(words[start:start + chunk_words]).strip()
            if part:
                chunks.append({"page": page["page"], "text": part})
            start += max(1, chunk_words - overlap)
    return chunks

def retrieve(question, chunks, top_k=3):
    if not chunks:
        return []
    corpus = [c["text"] for c in chunks]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=12000)
    matrix = vectorizer.fit_transform(corpus + [question])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    order = scores.argsort()[::-1][:top_k]
    return [{"page": chunks[i]["page"], "text": chunks[i]["text"], "score": float(scores[i])} for i in order if scores[i] > 0]

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text)) if len(s.strip()) > 35]

def summarize(text, max_sentences=7):
    sents = sentences(text)
    if not sents:
        return "No readable text was extracted."
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    freq = Counter(w for w in words if w not in STOP)
    scored = []
    for idx, sent in enumerate(sents):
        tokens = [w for w in re.findall(r"\b[a-zA-Z]{3,}\b", sent.lower()) if w not in STOP]
        score = sum(freq[w] for w in tokens) / max(len(tokens), 1)
        scored.append((score, idx, sent))
    chosen = sorted(sorted(scored, reverse=True)[:max_sentences], key=lambda x: x[1])
    return " ".join(x[2] for x in chosen)

def answer_from_chunks(question, matches):
    if not matches:
        return "I could not find a sufficiently relevant passage. Try using terms that appear in the PDF."
    pieces = []
    for m in matches:
        # Return the strongest source passages rather than inventing unsupported facts.
        pieces.append(f"**From page {m['page']}:** {m['text']}")
    return "\n\n".join(pieces) + "\n\n*Note: These are the most relevant passages retrieved from the PDF. Read the cited page for full context.*"

def make_flashcards(text, count=8):
    sents = sentences(text)
    cards = []
    for sent in sents:
        match = re.match(r"^(.{3,70}?)\s+(is|are|refers to|means|defined as|can be defined as)\s+(.+)$", sent, re.I)
        if match:
            term, _, definition = match.groups()
            cards.append({"question": f"What is {term.strip()}?", "answer": definition.strip()})
        elif len(sent.split()) >= 10:
            words = sent.split()
            key = next((w.strip(".,:;()") for w in words if len(w.strip(".,:;()")) > 7), words[0])
            cards.append({"question": f"What does the document explain about “{key}”?", "answer": sent})
        if len(cards) >= count:
            break
    return cards
