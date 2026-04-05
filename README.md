# 🚀 Q&A Semantic Search System (RAG-based)

## 📌 Overview
This project is a Semantic Search System for Question & Answer pairs using embeddings and vector databases.

It allows users to:
- Index Q&A datasets
- Perform semantic search (meaning-based, not keyword-based)
- Retrieve the most relevant answer instantly

The system uses:
- FastAPI → API backend
- Qdrant → Vector database
- Sentence Transformers → Embeddings
- Docker → Deployment

---

## 🧠 How It Works
1. Convert questions → embeddings
2. Store embeddings in Qdrant
3. Convert user query → embedding
4. Perform similarity search
5. Return best matching answer

---

## 🏗️ Architecture
- API Layer → FastAPI endpoints
- Service Layer → Business logic
- Embedding Layer → Vector generation
- Database Layer → Qdrant vector search

---

## 📂 Project Structure
.
├── api/
│   ├── server.py
│   ├── schemas.py
├── app/
│   ├── services.py
│   ├── config.py
├── data_base/
│   ├── repository.py
│   ├── operation.py
├── embedding_providers/
│   ├── base_provider.py
│   ├── hugging_face_provider.py
│   ├── embedding_provider_factory.py
├── processing.py
├── demo.py
├── test.py
├── docker-compose.yml
├── requirements.txt
├── dot.env
└── qa_pairs2.csv

---

## 🔌 API Endpoints

### Health Check
GET /health

### Stats
GET /stats

### Index Data
POST /index

### Query
POST /query

### Delete
DELETE /delete/{question_id}

### Clear
DELETE /clear

---

## 🐳 Run with Docker
docker-compose up --build

---

## ▶️ Run Locally
pip install -r requirements.txt
uvicorn api.server:app --reload

---

## 📥 Upload Dataset
python processing.py

---

## 🧪 Demo
python demo.py

---

## ⚙️ Environment Variables
QDRANT_HOST=qdrant
QDRANT_PORT=6333
COLLECTION_NAME=qa_pairs
EMBEDDING_MODEL=thenlper/gte-small
SIMILARITY_METRIC=cosine

---

## 📈 Features
- Semantic search (embedding-based)
- Fast vector retrieval (Qdrant)
- Batch indexing
- REST API (FastAPI)
- Docker deployment
- Clean architecture

---

## 📌 Future Improvements
- Add LLM → full RAG
- Return Top-K results
- Add frontend UI
- Add reranking model
- Add metadata filtering

---

## 👤 Author
Fares Hassan

---

## 🧾 Short Description
This project implements a semantic search system for question-answer pairs using embedding-based retrieval. It integrates FastAPI, Qdrant, and Sentence Transformers to provide efficient and scalable semantic search capabilities.
