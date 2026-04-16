import re
from bs4 import BeautifulSoup
from html import unescape

def mediawiki_cleaner_v1(raw_text):
  cleaned_docs = []

  docs = raw_text.split("[[[END]]]")

  for doc in docs:
    doc = doc.strip()
    if not doc:
        continue

    url_match = re.search(r"\[\[\[URL:(.*?)\]\]\]", doc)
    url = url_match.group(1) if url_match else None

    doc = re.sub(r"\[\[\[URL:.*?\]\]\]", "", doc)

    soup = BeautifulSoup(doc, "html.parser")

    main = soup.select_one("div.mw-parser-output")

    if main:
        content_root = main
    else:
        content_root = soup

    for tag in content_root(["script", "style", "noscript"]):
        tag.decompose()

    for tag in content_root.find_all(["table", "nav", "footer"]):
        classes = " ".join(tag.get("class", []))

        if any(x in classes for x in ["navbar", "footer", "mw-footer", "toc", "metadata"]):
            tag.decompose()

        text = content_root.get_text(separator="\n", strip=True)

        text = unescape(text)

        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = text.strip()

        if len(text) < 80:
            continue

        cleaned_docs.append({
            "url": url,
            "text": text
        })

    return cleaned_docs


with open("dataset_test.txt", "r", encoding="utf-8") as f:
    raw = f.read()

cleaned = mediawiki_cleaner_v1(raw)

for c in cleaned[:3]:
    print("\n" + "="*80)
    print(c["url"])
    print(c["text"][:800])

