from app.generator.llm_client import generate_response

class RAGPipeline:
    def __init__(self):
        from app.retriever.vector_store import VectorStore
        self.vs = VectorStore()
        self.vs.load()

    def query(self, question: str, top_k: int = 3):
        results = self.vs.search(question, k=top_k)
        context = "\n\n".join([r["chunk"] for r in results])
        
        prompt = (
            f"You are a helpful assistant answering questions about the U.S. secondary mortgage market, "
            f"particularly Fannie Mae and Freddie Mac. Use the context below to help answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\nAnswer:"
        )

        return generate_response(prompt)
