# Frontend UI

This directory contains the React application that serves as the conversational interface for the RAG Demo. It is built using Vite for fast bundling and hot module replacement.

## Prerequisites

- [Node.js](https://nodejs.org/) installed on your system.
- The Backend API running locally (see the [Backend README](../backend/README.md)).

## Setup

1. **Install Dependencies**
   Navigate to the `/frontend` directory and install the necessary Node modules:
   ```bash
   npm install
   ```

2. **Run the Development Server**
   Start the Vite development server:
   ```bash
   npm run dev
   ```

3. **Access the Application**
   Open your browser and navigate to the URL provided by Vite (typically `http://localhost:5173`). You can now start querying your ebooks!

## Important Notes

- **CORS Configuration:** The frontend communicates directly with the FastAPI backend (expected to be on `http://127.0.0.1:8000`). If your backend is running on a different port, ensure you update the fetch URLs in the React components.
