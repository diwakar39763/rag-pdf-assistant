import streamlit as st
import requests

# ==================================
# Backend URL
# ==================================

BACKEND_URL = "http://backend:8001"
# ==================================
# Session State
# ==================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==================================
# Page Config
# ==================================

st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="📄",
    layout="wide"
)

# ==================================
# Title
# ==================================

st.title("📄 AI PDF Assistant")
st.write("Ask questions from your PDF using RAG + Llama3")

# ==================================
# Sidebar
# ==================================

with st.sidebar:

    st.header("⚙️ About")

    st.write("""
    ### Tech Stack
    
    - FastAPI
    - Streamlit
    - Qdrant
    - Ollama
    - Llama3
    - Sentence Transformers
    - RAG Architecture
    """)

    st.write("---")

    if st.button("🗑️ Clear Chat"):

        st.session_state.chat_history = []

        st.success("Chat history cleared")

# ==================================
# Upload PDF Section
# ==================================

st.write("## 📤 Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:

    with st.spinner("Uploading and processing PDF..."):

        response = requests.post(
            f"{BACKEND_URL}/upload-pdf",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }
        )

    if response.status_code == 200:

        result = response.json()

        st.success("✅ PDF uploaded successfully!")

        st.write(f"Filename: {result['filename']}")

        st.write(f"Total Chunks: {result['total_chunks']}")

    else:

        st.error("❌ Error uploading PDF")

# ==================================
# Ask Question Section
# ==================================

st.write("---")
st.write("## 🤖 Ask Questions")

question = st.text_input(
    "Enter your question"
)

if st.button("Ask AI"):

    if question:

        # Show User Message
        st.chat_message("user").write(question)

        # API Call
        with st.spinner("Thinking..."):

            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={
                    "question": question
                }
            )

        # Success
        if response.status_code == 200:

            result = response.json()

            answer = result["answer"]

            retrieved_chunks = result["retrieved_chunks"]

            # Show AI Answer
            st.chat_message("assistant").write(answer)

            # Save Chat History
            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

            # Retrieved Chunks
            st.write("## 📚 Retrieved Chunks")

            for chunk in retrieved_chunks:

                st.write("---")

                st.write(
                    f"Similarity Score: {chunk['score']:.4f}"
                )

                st.info(chunk["text"])

        else:

            st.error("❌ Error generating answer")

# ==================================
# Chat History Section
# ==================================

st.write("---")
st.write("## 🕘 Chat History")

if len(st.session_state.chat_history) == 0:

    st.write("No chat history yet.")

else:

    for chat in reversed(st.session_state.chat_history):

        st.write("---")

        st.write(f"🧑 Question: {chat['question']}")

        st.write(f"🤖 Answer: {chat['answer']}")