import re
from bs4 import BeautifulSoup
from html import unescape

INPUT_FILE = "Raw_Med_Data.txt"
OUTPUT_FILE = "Cleaned_Med_Data.txt"


def is_garbage(text):
    lines = text.split("\n")

    short_lines = sum(1 for l in lines if len(l.strip()) < 40)
    long_lines = sum(1 for l in lines if len(l.strip()) > 120)

    if short_lines > long_lines * 4:
        return True

    words = re.findall(r"\w+", text.lower())
    if len(words) > 0:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.2:
            return True

    return False


def clean_html_safe(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    text = unescape(text)

    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    lines = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if len(line) <= 1:
            continue

        lines.append(line)

    text = "\n".join(lines)

    if is_garbage(text):
        return None

    return text


def process_file():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = f.read()

    # 🔥 split podľa URL (nie END)
    chunks = re.split(r"={3,}\s*URL:", data)

    count = 0
    kept = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:

        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue

            header = re.match(r"(.*?)\s*\|\s*TYPE:\s*(.*?)\s*===\n", chunk)
            if not header:
                continue

            url = header.group(1).strip()
            typ = header.group(2).strip()

            html = chunk[header.end():]

            text = clean_html_safe(html)

            count += 1

            if not text:
                continue

            out.write("=" * 80 + "\n")
            out.write(f"{url} | {typ}\n")
            out.write(text + "\n\n")

            kept += 1

            if count % 100 == 0:
                print(f"Processed: {count} | Kept: {kept}")

    print(f"\nDONE: {count} docs | KEPT: {kept}")


if __name__ == "__main__":
    process_file()
