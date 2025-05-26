import json
from app.scraper.fannie_freddie_scraper import (
    scrape_fannie_newsroom,
    scrape_freddie_bulletins
)

def main():
    print("Scraping Fannie Mae...")
    fannie_articles = scrape_fannie_newsroom(limit=10)

    print("Scraping Freddie Mac...")
    freddie_bulletins = scrape_freddie_bulletins(limit=10)

    all_docs = fannie_articles + freddie_bulletins

    # Save to /data
    with open("data/raw_documents.json", "w", encoding="utf-8") as f:
        json.dump(all_docs, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(all_docs)} documents to data/raw_documents.json")

if __name__ == "__main__":
    main()
