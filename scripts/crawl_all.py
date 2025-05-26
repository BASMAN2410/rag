import json
from app.scraper.full_crawler import crawl_domain

def main():
    print("📡 Crawling Fannie Mae...")
    fannie_docs = crawl_domain("https://www.fanniemae.com", "https://www.fanniemae.com", limit=200)

    print("📡 Crawling Freddie Mac...")
    freddie_docs = crawl_domain("https://www.freddiemac.com", "https://www.freddiemac.com", limit=200)

    all_docs = fannie_docs + freddie_docs
    with open("data/raw_documents.json", "w", encoding="utf-8") as f:
        json.dump(all_docs, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(all_docs)} documents to data/raw_documents.json")

if __name__ == "__main__":
    main()
