import json
import os
from full_crawler_enhanced import crawl_domain

def crawl_and_save(name, start_url, domain, limit=200):
    output_path = f"data/{name}_raw_documents.json"
    checkpoint_path = f"data/{name}_checkpoint.json"

    print(f"📡 Crawling {name.title()}...")
    docs = crawl_domain(start_url, domain, limit=limit, checkpoint_path=checkpoint_path)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)

    print(f"✅ {name.title()} crawl complete. Saved {len(docs)} documents to {output_path}")
    return docs

def combine_and_save(docs_list, combined_path="data/raw_documents.json"):
    all_docs = [doc for docs in docs_list for doc in docs]
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(all_docs, f, indent=2, ensure_ascii=False)
    print(f"✅ Combined and saved {len(all_docs)} total documents to {combined_path}")

def rebuild_faiss():
    print("🔧 Rebuilding FAISS index...")
    from app.retriever.vector_store import VectorStore
    vs = VectorStore()
    vs.build_index_from_json("data/raw_documents.json")
    vs.save()
    print("✅ FAISS index rebuilt and saved to data/faiss_index/")

if __name__ == "__main__":
    fannie_docs = crawl_and_save("fannie", "https://www.fanniemae.com", "https://www.fanniemae.com", limit=500)
    freddie_docs = crawl_and_save("freddie", "https://www.freddiemac.com", "https://www.freddiemac.com", limit=500)

    combine_and_save([fannie_docs, freddie_docs])
    rebuild_faiss()
