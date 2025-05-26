import os
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def chunk_text(self, text: str, chunk_size: int = 5):
        """
        Splits text into sentence chunks (e.g., 5 sentences per chunk).
        """
        sentences = sent_tokenize(text)
        chunks = []
        for i in range(0, len(sentences), chunk_size):
            chunk = " ".join(sentences[i:i + chunk_size])
            chunks.append(chunk)
        return chunks

    def embed_chunks(self, chunks: list[str]):
        """
        Returns embeddings for a list of text chunks.
        """
        return self.model.encode(chunks)

    def embed_document(self, text: str, chunk_size: int = 5):
        """
        Full process: chunk + embed
        Returns:
            chunks (list[str]), embeddings (ndarray)
        """
        chunks = self.chunk_text(text, chunk_size)
        embeddings = self.embed_chunks(chunks)
        return chunks, embeddings
