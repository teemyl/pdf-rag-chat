# Backend API & Data Ingestion

This directory contains the FastAPI server that powers the RAG Demo, as well as the script responsible for ingesting PDFs into the Qdrant vector database.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your system.
- Qdrant running via Docker (see the [Root README](../README.md)).

## Setup

1. **Environment Variables**
   Create a `.env` file in this `/backend` directory and add your Anthropic API key:
   ```env
   ANTHROPIC_API_KEY="your_api_key_here"
   QDRANT_URL="http://localhost:6333"
   ```

2. **Install Dependencies**
   (Optional but recommended: uv will automatically handle dependencies when you run the commands below, but you can explicitly sync the environment):
   ```bash
   uv sync
   ```

## Ingesting Data

Before chatting, you need to populate the vector database with your ebooks.

1. Place your PDF files in a `/data` directory at the root of the project (i.e., `../data`).
2. Run the ingestion script:
   ```bash
   uv run python ingest.py
   ```
   This script will chunk the PDFs, embed them using HuggingFace models, and store them in Qdrant.

## Running the Server

Start the FastAPI development server:

```bash
uv run fastapi dev main.py
```

The API will be available at `http://127.0.0.1:8000`. You can test the endpoints or view the interactive Swagger UI at `http://127.0.0.1:8000/docs`.
