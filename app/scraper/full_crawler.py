import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

def crawl_domain(start_url, domain, limit=100):
    visited = set()
    queue = [start_url]
    documents = []

    while queue and len(visited) < limit:
        url = queue.pop(0)
        if url in visited or not url.startswith(domain):
            continue

        try:
            res = requests.get(url, headers=headers, timeout=10)
            if "text/html" not in res.headers.get("Content-Type", ""):
                continue

            visited.add(url)
            soup = BeautifulSoup(res.content, "lxml")
            paragraphs = soup.select("p")
            text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            if text:
                documents.append({"url": url, "text": text})

            # Add more internal links
            for link in soup.find_all("a", href=True):
                href = link['href']
                full_url = urljoin(url, href)
                if urlparse(full_url).netloc == urlparse(domain).netloc:
                    queue.append(full_url)

            time.sleep(1)  # respectful crawling

        except Exception as e:
            print(f"Failed: {url} - {e}")
            continue

    return documents
