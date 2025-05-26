import json
import os
import faiss
import numpy as np
from app.retriever.embedder import Embedder

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embedder = Embedder(model_name)
        self.index = None
        self.text_chunks = []  # List of text chunks
        self.metadata = []     # List of {source_url, chunk_index}

    def build_index_from_json(self, json_path: str):
        with open(json_path, "r", encoding="utf-8") as f:
            documents = json.load(f)

        all_embeddings = []
        for doc in documents:
            chunks, vectors = self.embedder.embed_document(doc["text"])
            self.text_chunks.extend(chunks)
            all_embeddings.extend(vectors)
            self.metadata.extend([
                {"url": doc["url"], "chunk_index": i}
                for i in range(len(chunks))
            ])

        embedding_dim = len(all_embeddings[0])
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(np.array(all_embeddings).astype("float32"))
    
    # This method saves the FAISS index and metadata to specified paths.
    def save(self, index_path="data/faiss_index/index.faiss", metadata_path="data/faiss_index/meta.json"):
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(self.index, index_path)

        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump({
                "chunks": self.text_chunks,
                "metadata": self.metadata
            }, f, indent=2, ensure_ascii=False)

    def load(self, index_path="data/faiss_index/index.faiss", metadata_path="data/faiss_index/meta.json"):
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            self.text_chunks = meta["chunks"]
            self.metadata = meta["metadata"]

    def search(self, query: str, k: int = 3):
        query_embedding = self.embedder.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype("float32"), k)
        results = []
        for idx in indices[0]:
            results.append({
                "chunk": self.text_chunks[idx],
                "meta": self.metadata[idx]
            })
        return results
