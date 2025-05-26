import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_fannie_newsroom(limit=5):
    url = "https://www.fanniemae.com/newsroom"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "lxml")

    links = [a["href"] for a in soup.select("a") if a.has_attr("href") and a["href"].startswith("/newsroom/")]
    unique_links = list(set(links))[:limit]

    articles = []
    for link in tqdm(unique_links, desc="Scraping Fannie Mae"):
        full_url = f"https://www.fanniemae.com{link}"
        try:
            page = requests.get(full_url, headers=headers)
            content = BeautifulSoup(page.content, "lxml")
            paragraphs = content.select("article p")
            text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            if text:
                articles.append({"url": full_url, "text": text})
        except Exception as e:
            print(f"Failed: {full_url} - {e}")

    return articles

def scrape_freddie_bulletins(limit=5):
    base_url = "https://guide.freddiemac.com/app/guide/bulletins"
    res = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(res.content, "lxml")

    links = [a["href"] for a in soup.select("a") if a.has_attr("href") and a["href"].startswith("/app/guide/bulletin/")]
    unique_links = list(set(links))[:limit]

    bulletins = []
    for link in tqdm(unique_links, desc="Scraping Freddie Mac"):
        full_url = f"https://guide.freddiemac.com{link}"
        try:
            page = requests.get(full_url, headers=headers)
            content = BeautifulSoup(page.content, "lxml")
            text = "\n".join(p.get_text(strip=True) for p in content.select("main p"))
            if text:
                bulletins.append({"url": full_url, "text": text})
        except Exception as e:
            print(f"Failed: {full_url} - {e}")

    return bulletins
