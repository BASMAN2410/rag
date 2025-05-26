from app.retriever.vector_store import VectorStore

def main():
    vs = VectorStore()
    vs.build_index_from_json("data/raw_documents.json")
    vs.save()
    print("FAISS index and metadata saved to data/faiss_index/")

if __name__ == "__main__":
    print("Starting build_index.py")
    main()
