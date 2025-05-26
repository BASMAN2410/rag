# rag
# Tech stack- Deepseek 1.3B, Ollama
# activate virtual environment
# ragvirtualenv\Scripts\activate(cmd prompt) or .\ragvirtualenv\Scripts\Activate.ps1 (powershell)
# to deativate virtual environment - deactivate (both cmd prompt and cmd shell)
# to set scripts path for the session - set PYTHONPATH=C:\Users\baska\bas-rag\rag\scripts
# Packages used in the RAG
# To run streamlit - streamlit run app/ui/chat_app.py --server.runOnSave false
# add this to the config file to not use above command
# [server]
# folderWatchBlacklist = ["*"]
| Package                              | Purpose                                                             |
| ------------------------------------ | ------------------------------------------------------------------- |
| `sentence-transformers`              | Convert text to vector embeddings (e.g., `all-MiniLM` or `e5-base`) |
| `faiss-cpu`                          | Perform fast similarity search on embeddings                        |
| `beautifulsoup4`, `lxml`, `requests` | Scrape and parse HTML content                                       |
| `nltk`                               | Split text into chunks using sentence boundaries                    |
| `flask`                              | (Optional) Serve your RAG as an API                                 |
| `tqdm`                               | Progress bars during scraping or indexing                           |
| `python-dotenv`                      | Store configs like model name, Ollama URL, etc.                     |
Rag Project Structure
rag-project/
├── app/
│   ├── __init__.py
│   ├── main.py              # API (FastAPI/Flask) or entrypoint
│   ├── retriever/
│   │   ├── __init__.py
│   │   ├── vector_store.py  # FAISS or Elasticsearch integration
│   │   └── embedder.py      # SentenceTransformer or OpenAI embedding
│   ├── generator/
│   │   ├── __init__.py
│   │   └── deepseek_llm.py  # Ollama or Hugging Face model call
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── rag_chain.py     # Retrieves → constructs prompt → calls LLM
│   └── utils/
│       ├── __init__.py
│       └── logger.py        # Logging, config helpers, etc.
│
├── data/
│   ├── documents.json       # Preloaded or ingestable documents
│   └── faiss_index/         # FAISS index (persisted)
│
├── notebooks/
│   └── test_pipeline.ipynb  # Manual exploration/testing
│
├── tests/
│   ├── test_retriever.py
│   ├── test_generator.py
│   └── test_pipeline.py
│
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
