from app.pipeline.rag_chain import RAGPipeline

def main():
    rag = RAGPipeline()
    print("✅ RAG system ready. Ask questions about Fannie Mae or Freddie Mac.\nType 'exit' to quit.\n")

    while True:
        question = input("🧠 Your Question: ")
        if question.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        try:
            answer = rag.query(question)
            print("\n🤖 Answer:\n", answer, "\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()
