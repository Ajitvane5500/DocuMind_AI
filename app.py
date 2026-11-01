import streamlit as st
from src.pdf_engine import extract_pdf, make_chunks, retrieve, summarize, make_flashcards, answer_from_chunks

st.set_page_config(page_title="DocuMind AI", page_icon="📚", layout="wide")
st.title("📚 DocuMind AI — Intelligent PDF Assistant")
st.caption("Upload a PDF, ask questions, generate concise summaries and study flashcards.")

with st.sidebar:
    st.header("How it works")
    st.markdown("1. Upload a PDF\n2. The app extracts text and splits it into page-aware chunks\n3. Ask questions or generate study material\n4. Review the source page references")
    st.info("Privacy: PDFs are processed in this app session. Do not upload confidential documents to a public deployment.")

uploaded = st.file_uploader("Upload your PDF document", type=["pdf"])
if uploaded:
    try:
        pages = extract_pdf(uploaded.getvalue())
        full_text = "\n".join(p["text"] for p in pages if p["text"].strip())
        if not full_text.strip():
            st.error("No selectable text was found. This PDF may be scanned; OCR is not included in this version.")
            st.stop()
        chunks = make_chunks(pages)
        st.success(f"PDF processed: {len(pages)} pages, {len(chunks)} text sections.")
        tab1, tab2, tab3 = st.tabs(["💬 Ask a question", "📝 Executive summary", "🧠 Flashcards"])

        with tab1:
            question = st.text_input("Ask something about your PDF", placeholder="Example: What are the main objectives?")
            top_k = st.slider("Number of relevant sections", 1, 6, 3)
            if st.button("Get answer", type="primary", disabled=not question.strip()):
                matches = retrieve(question, chunks, top_k=top_k)
                answer = answer_from_chunks(question, matches)
                st.markdown("### Answer")
                st.write(answer)
                st.markdown("### Sources")
                for item in matches:
                    with st.expander(f"Page {item['page']} · relevance {item['score']:.2f}"):
                        st.write(item["text"])

        with tab2:
            max_sentences = st.slider("Summary length (sentences)", 3, 15, 7)
            if st.button("Generate summary"):
                st.markdown("### Executive summary")
                st.write(summarize(full_text, max_sentences=max_sentences))
                st.caption("This is an extractive summary assembled from the document's most informative sentences.")

        with tab3:
            count = st.slider("Number of flashcards", 3, 20, 8)
            if st.button("Create flashcards"):
                cards = make_flashcards(full_text, count=count)
                if not cards:
                    st.warning("Not enough readable text to create flashcards.")
                for i, card in enumerate(cards, 1):
                    with st.expander(f"Flashcard {i}: {card['question']}"):
                        st.write(f"**Answer:** {card['answer']}")
    except Exception as e:
        st.error(f"Could not process this PDF: {e}")
else:
    st.info("👆 Choose a PDF file to begin.")
    st.markdown("**Features:** PDF text extraction · relevant passage retrieval · question answering with page references · executive summaries · flashcards")
