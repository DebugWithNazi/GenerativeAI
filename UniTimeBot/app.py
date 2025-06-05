# ===============================
# 📦 Install dependencies (Only for Colab)
# ===============================
# !pip install streamlit faiss-cpu PyPDF2 sentence-transformers

# ===============================
# 📄 Imports
# ===============================
import os
import numpy as np
import PyPDF2
import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss

# ✅ Set Streamlit page configuration at the top
st.set_page_config(
    page_title="📅 Exam Schedule Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ===============================
# 🎨 Styling
# ===============================
st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            font-weight: 800;
            color: #1f77b4;
            text-align: center;
        }
        .sub-title {
            font-size: 20px;
            color: #555;
            text-align: center;
        }
        .stTextInput > div > input {
            font-size: 16px;
            height: 3em;
        }
        .stFileUploader {
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ===============================
# 🧠 Load PDF & Extract Text
# ===============================
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# ===============================
# 🧩 Embed Text and Create FAISS Index
# ===============================
def embed_and_index(text, model):
    chunks = text.split("\n")
    docs = [chunk.strip() for chunk in chunks if chunk.strip()]
    vectors = model.encode(docs, convert_to_tensor=False)
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors))
    return docs, index

# ===============================
# 🤖 Query with Context
# ===============================
def query_with_context(question, docs, index, model):
    question_vec = model.encode([question], convert_to_tensor=False)
    D, I = index.search(np.array(question_vec), k=3)
    context = "\n".join([docs[i] for i in I[0]])
    return f"📌 **Relevant Information:**\n\n{context}"

# ===============================
# 💬 UI
# ===============================
st.markdown('<div class="main-title">📅 University Exam Schedule Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Ask questions like "When is the AI exam?" or "Date of Software Engineering paper?"</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload your Date Sheet PDF", type="pdf")
query = st.text_input("❓ Ask something about your exam schedule:")

if uploaded_file and query:
    if 'docs' not in st.session_state:
        text = extract_text_from_pdf(uploaded_file)
        model = SentenceTransformer("all-MiniLM-L6-v2")
        st.session_state.docs, st.session_state.index = embed_and_index(text, model)
        st.session_state.embedding_model = model

    answer = query_with_context(
        query,
        st.session_state.docs,
        st.session_state.index,
        st.session_state.embedding_model
    )

    st.markdown("### 💬 Answer:")
    st.success(answer)
