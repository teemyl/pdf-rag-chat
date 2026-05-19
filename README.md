# Ebook RAG Demo

A personal Retrieval-Augmented Generation (RAG) knowledge base built to ingest and chat with specific ebooks. 

This project demonstrates a full-stack, AI-powered conversational interface using local vector embeddings for cost-efficiency and Anthropic's Claude for high-quality reasoning.

## Tech Stack & Architecture

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python) managed by `uv`.
- **Frontend:** [React](https://react.dev/) + [Vite](https://vitejs.dev/).
- **AI & Orchestration:** [LangChain](https://python.langchain.com/) + [Claude 3.5 Sonnet](https://www.anthropic.com/claude).
- **Vector Database:** [Qdrant](https://qdrant.tech/) running via Docker.
- **Embeddings:** Local HuggingFace embeddings (`BAAI/bge-small-en-v1.5`) for fast, private, and cost-effective document vectorization without hitting external API limits during ingestion.

## Project Structure

This repository is split into distinct services:

- `/backend` - The FastAPI server and document ingestion scripts. See the [Backend README](./backend/README.md) for setup details.
- `/frontend` - The React user interface. See the [Frontend README](./frontend/README.md) for setup details.

## Quick Start (Infrastructure)

To run the full stack, you will need **Docker**, **Node.js**, and **uv** (Python package manager).

### 1. Start the Vector Database

The Qdrant vector database runs locally via Docker Compose. From the root directory:

```bash
docker compose up -d
```

This will start Qdrant on `http://localhost:6333` and persist data to `./qdrant_storage`.

### 2. Start the Backend API

See the [Backend README](./backend/README.md) for instructions on setting up environment variables, ingesting your PDFs, and starting the FastAPI server.

### 3. Start the Frontend UI

See the [Frontend README](./frontend/README.md) for instructions on starting the Vite development server.
