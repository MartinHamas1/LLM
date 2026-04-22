import re
from bs4 import BeautifulSoup
from html import unescape

INPUT_FILE = "Raw_Med_Data.txt"
OUTPUT_FILE = "Cleaned_Med_Data.txt"


def normalize_text(text):
    text = unescape(text)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    lines = []
    seen = set()

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if len(line) == 1:
            continue

        if line in seen:
            continue

        seen.add(line)
        lines.append(line)

    return "\n".join(lines)


def extract_main_content(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    for tag in soup.find_all(["nav", "footer", "header", "form"]):
        tag.decompose()

    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", class_=re.compile("content|mw-parser-output|main"))
    )

    if main:
        content = main
    else:
        content = soup

    text = content.get_text(separator="\n", strip=True)

    return normalize_text(text)


def process_stream():
    buffer = ""
    count = 0
    kept = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as f, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as out:

        for line in f:
            buffer += line

            if "=== END ===" not in buffer:
                continue

            parts = buffer.split("=== END ===")

            for part in parts[:-1]:
                part = part.strip()
                if not part:
                    continue

                header = re.search(r"=== URL: (.*?) \| TYPE: (.*?) ===", part)
                if not header:
                    continue

                url = header.group(1).strip()
                typ = header.group(2).strip()

                html = re.sub(r"^.*?===\n?", "", part, flags=re.DOTALL)

                text = extract_main_content(html)

                count += 1

                if not text or len(text) < 20:
                    continue

                out.write("=" * 80 + "\n")
                out.write(f"{url} | {typ}\n")
                out.write(text + "\n\n")

                kept += 1

                if count % 100 == 0:
                    print(f"Processed: {count} | Kept: {kept}")

            buffer = parts[-1]

    print(f"DONE: {count} | KEPT: {kept}")


if __name__ == "__main__":
    process_stream()
