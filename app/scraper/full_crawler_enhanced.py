import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import io
import fitz  # PyMuPDF
from tqdm import tqdm
import json

headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_pdf_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        pdf_stream = io.BytesIO(response.content)
        doc = fitz.open(stream=pdf_stream, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()

        return text.strip()

    except Exception as e:
        print(f"❌ Failed to extract PDF: {url} - {e}")
        return None

def crawl_domain(start_url, domain, limit=100, checkpoint_path=None):
    visited = set()
    queue = [start_url]
    documents = []

    with tqdm(total=limit, desc=f"Crawling {urlparse(domain).netloc}") as pbar:
        while queue and len(visited) < limit:
            url = queue.pop(0)
            if url in visited or not url.startswith(domain):
                continue

            try:
                if url.endswith(".pdf"):
                    text = extract_pdf_text_from_url(url)
                    if text:
                        documents.append({"url": url, "text": text})
                        visited.add(url)
                        pbar.update(1)
                    continue

                res = requests.get(url, headers=headers, timeout=10)
                if "text/html" not in res.headers.get("Content-Type", ""):
                    continue

                visited.add(url)
                soup = BeautifulSoup(res.content, "lxml")
                paragraphs = soup.select("p")
                text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                if text:
                    documents.append({"url": url, "text": text})
                    pbar.update(1)

                for link in soup.find_all("a", href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    if urlparse(full_url).netloc == urlparse(domain).netloc:
                        queue.append(full_url)

                time.sleep(5)

                if checkpoint_path and len(documents) % 10 == 0:
                    with open(checkpoint_path, "w", encoding="utf-8") as f:
                        json.dump(documents, f, indent=2, ensure_ascii=False)

            except Exception as e:
                print(f"Failed: {url} - {e}")
                continue

    return documents

if __name__ == "__main__":
    start_url = "https://www.fanniemae.com"
    domain = "https://www.fanniemae.com"
    limit = 200
    output_path = "data/fannie_raw_documents.json"
    checkpoint_path = "data/fannie_checkpoint.json"

    docs = crawl_domain(start_url, domain, limit=limit, checkpoint_path=checkpoint_path)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)

    print(f"✅ Crawl complete. Saved {len(docs)} documents to {output_path}")
