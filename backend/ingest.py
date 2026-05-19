import os
import glob
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import PyPDFLoader

# Load environment variables
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "ebooks"

def ingest_pdfs(data_dir="../data"):
    # Ensure data directory exists
    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} does not exist. Creating it...")
        os.makedirs(data_dir)
        print("Please place your PDF ebooks in the 'data' directory and run again.")
        return

    # Find all PDFs
    pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {data_dir}.")
        return

    print(f"Found {len(pdf_files)} PDF(s). Loading...")
    docs = []
    for file_path in pdf_files:
        print(f"Loading {file_path}...")
        loader = PyPDFLoader(file_path)
        docs.extend(loader.load())

    print(f"Total pages loaded: {len(docs)}")

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    splits = text_splitter.split_documents(docs)

    print(f"Split into {len(splits)} chunks.")

    # Initialize Embeddings
    print("Initializing HuggingFace embeddings (this might download the model on first run)...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    # Upsert to Qdrant
    print(f"Connecting to Qdrant at {QDRANT_URL}...")

    qdrant = QdrantVectorStore.from_documents(
        documents=splits,
        embedding=embeddings,
        url=QDRANT_URL,
        prefer_grpc=False,
        collection_name=COLLECTION_NAME,
        force_recreate=True, # Note: this will wipe the existing collection on every run
    )

    print("Ingestion complete! Data is now in Qdrant.")

if __name__ == "__main__":
    ingest_pdfs()
