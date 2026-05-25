# AI PDF Assistant (RAG Project)

This project is a complete RAG (Retrieval-Augmented Generation) application using:

- FastAPI
- Streamlit
- Qdrant
- Ollama
- Llama3
- Docker

## Features

- Upload PDFs
- Extract text
- Generate embeddings
- Store vectors in Qdrant
- Ask questions about PDFs
- Conversational memory
- Dockerized deployment

## Run Project

```bash
docker compose up --build

Frontend:
http://localhost:8501

Backend:
http://localhost:8001

Frontend:

http://localhost:8501

Backend:

http://localhost:8001/docs

Qdrant:

http://localhost:6333/dashboard