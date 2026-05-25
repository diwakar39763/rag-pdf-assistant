from fastapi import FastAPI, UploadFile, File
from embedding_generator import generate_embedding
from text_chunker import chunk_text
from qdrant_manager import (
    create_collection,
    store_embedding,
    search_similar_chunks
)
from pydantic import BaseModel
from llm_generator import generate_answer

import shutil
import os

from pdf_reader import extract_text_from_pdf

# ==================================
# FastAPI App
# ==================================

app = FastAPI()

create_collection()

# ==================================
# Upload Folder
# ==================================

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==================================
# Request Model
# ==================================

class QuestionRequest(BaseModel):
    question: str

# ==================================
# Home Route
# ==================================

@app.get("/")
def home():

    return {
        "message": "RAG Project Running"
    }

# ==================================
# Upload PDF Route
# ==================================

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    # Save PDF
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract text
    extracted_text = extract_text_from_pdf(file_path)

    # Create chunks
    chunks = chunk_text(extracted_text)

    # Generate embeddings and store
    for index, chunk in enumerate(chunks):

        embedding = generate_embedding(chunk)

        store_embedding(
            chunk_id=index,
            embedding=embedding,
            text=chunk
        )

    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "message": "Embeddings stored successfully in Qdrant"
    }

# ==================================
# Ask Question Route
# ==================================

@app.post("/ask")
async def ask_question(request: QuestionRequest):

    question = request.question

    # Generate query embedding
    query_embedding = generate_embedding(question)

    # Search similar chunks
    results = search_similar_chunks(query_embedding)

    retrieved_chunks = []

    context_text = ""

    # Build context
    for result in results:

        chunk_text_data = result.payload["text"]

        retrieved_chunks.append(
            {
                "score": result.score,
                "text": chunk_text_data
            }
        )

        context_text += chunk_text_data + "\n"

    # Conversation history
    history = ""

    # Generate final answer
    answer = generate_answer(
        context_text,
        question,
        history
    )

    return {
        "answer": answer,
        "retrieved_chunks": retrieved_chunks
    }