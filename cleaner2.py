import re

INPUT_FILE = "Cleaned_Med_Data.txt"
OUTPUT_FILE = "Final_Med_Data.txt"


def remove_blocks(text):
    patterns = [
        r"Jak jste spokojeni.*?Sdílejte pojem",
        r"Vaše zpětná vazba.*?Text zprávy",
        r"Najdete na NZIP.*?Sledujte nás",
        r"WikiSkripta.*?Potřebujete pomoc\?",
    ]

    for p in patterns:
        text = re.sub(p, "", text, flags=re.DOTALL | re.IGNORECASE)

    return text


def clean_lines(text):
    lines = []
    seen = set()

    garbage_phrases = [
        "národní zdravotnický informační portál",
        "data, grafy a vizualizace",
        "vybrané články",
        "ze světa zdraví",
        "životní situace",
        "prevence a zdravý životní styl",
        "informace o nemocech",
        "mapa zdravotní péče",
        "rejstřík pojmů",
        "doporučené weby",
        "datové zpravodajství",
        "napište nám",
        "menu",
        "přihlaste se",
        "osobní nástroje",
        "diskuse",
        "příspěvky",
        "vytvořit účet",
        "potřebujete pomoc",
        "sledovat nás",
        "newsletter",
        "cookie",
        "prohlášení",
        "často kladené dotazy",
        "kdo jsme",
        "více",
        "chci vědět více"
        "rady a doporučení",
        "hlavní zásady",
        "základní fakta",
        "najdi nejbližšího lékaře",
        "interaktivní vzdělávání",
        "krátká vysvětlení pro laickou veřejnost",
        "online informační servis",
        "mohlo by",
        "vás zajímat",
        "najděte svého průvodce zdravím",
        "praktické a odborně garantované informace",
        "ezkarta",
        "digitální služby zdravotnictví",
        "minianketa",
        "vyplnit anketu",
        "vaše odpovědi nám pomohou",
        "o nzip",
        "co je nzip",
        "ověřeno odborníky",
        "srozumitelně pro každého",
        "od prevence po léčbu",
        "propojujeme svět zdraví",
        "co na nzip najdete",
        "doporučené zdroje",
        "najděte nejbližšího specialistu",
        "interaktivní kvízy",
        "kdo za nzip stojí",
        "zapojené organizace",
        "co říkají naši čtenáři",
        "podmínky užití",
        "jak pracujeme s online zdroji",
        "licence a využití obsahu",
        "projektová podpora",
        "operační program",
        "číslo projektu",
        "celkový rozpočet",
        "o nzis open",
        "co je nzis",
        "publikační platforma",
        "proč nzis open",
        "ověřená data",
        "komunita",
        "datově řízená rozhodnutí",
        "katalog zdravotnických dat",
        "průvodce zdravotnickými daty",
        "žádosti o data",
        "data hrou",
        "agendy a zdroje nzis",
        "konference nzip",
        "syntetická data",
        "nzis open journal",
        "tematické portály",
        "co říkají uživatelé našich dat",
        "kdo za nzis open stojí",
        "příběh nzis open",
        "prozkoumejte dále",
        "zůstaňte v obraze",
        "datové novinky",
        "linkedin",
        "máte nějaké otázky",
        "uživatelské testování",
    ]

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if set(line) == {"="}:
            continue

        if "http" in line:
            continue

        # --- NOVÉ CLEANINGY ---
        line = re.sub(r'https?://\S+|www\.\S+', '', line)
        line = re.sub(r'\|\s*(low|medium|high)', '', line, flags=re.IGNORECASE)
        line = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '', line)
        line = re.sub(r'\b\d{1,2}\.\s?\d{1,2}\.\s?\d{2,4}\b', '', line)
        line = re.sub(r'CZ\.\d+\.\d+\.\d+/\d+_\d+/\d+', '', line)
        line = re.sub(r'\b(prof|doc|mudr|mgr|ing|bc|phdr|rndr)\.?\s+[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž]+', '', line, flags=re.IGNORECASE)
        line = re.sub(r'\b(prof|doc|mudr|mgr|ing|bc|phdr|rndr)\.?\s*', '', line, flags=re.IGNORECASE)
        line = re.sub(r'\b\d{1,3}(?:\s?\d{3})+\s?(Kč)?\b', '', line)
        line = re.sub(r'\s+', ' ', line).strip()

        low = line.lower()

        if any(p in low for p in garbage_phrases):
            continue

        if len(line) < 5:
            continue

        if line in seen:
            continue

        seen.add(line)
        lines.append(line)

    return "\n".join(lines)


def process():
    print("START SECOND CLEANING...")

    count = 0

    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as out:

        buffer = []

        for line in f:
            if line.strip() == "":
                if buffer:
                    text = "\n".join(buffer)
                    text = remove_blocks(text)
                    text = clean_lines(text)

                    if text.strip():
                        out.write(text + "\n\n")

                    buffer = []
                    count += 1

                    if count % 50 == 0:
                        print(f"Processed: {count}")
            else:
                buffer.append(line.strip())

        if buffer:
            text = "\n".join(buffer)
            text = remove_blocks(text)
            text = clean_lines(text)

            if text.strip():
                out.write(text + "\n\n")

            count += 1

    print(f"DONE: {count} documents")


if __name__ == "__main__":
    process()
