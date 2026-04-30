import re
from bs4 import BeautifulSoup

def simple_extractor(input_file, output_file):
    print(f"Spúšťam extrakciu jadra z {input_file}...")
    
    # Použijeme generátor, aby sme nenačítali celých 650MB do RAM naraz
    def article_generator(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            current_article = []
            for line in f:
                if line.startswith("=== END ==="):
                    yield "".join(current_article)
                    current_article = []
                else:
                    current_article.append(line)

    count = 0
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for raw_content in article_generator(input_file):
            if not raw_content.strip():
                continue
                
            # Extrakcia URL (vždy na začiatku tvojho formátu)
            url_match = re.search(r"=== URL: (.*?) \|", raw_content)
            url = url_match.group(1) if url_match else "Neznámy zdroj"
            
            # Odstránime tvoje hlavičky z crawllera
            clean_html = re.sub(r"=== URL:.*?===", "", raw_content, flags=re.DOTALL)
            
            soup = BeautifulSoup(clean_html, 'html.parser')
            
            # 1. ODSTRÁNENIE JADROVÉHO ODPADU (to čo v modeli nikdy nechceme)
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
                element.decompose()

            # 2. ZÍSKANIE TEXTU 
            # separator=' ' zabezpečí, že sa slová nezlepia (napr. z <div>Slovo1</div><div>Slovo2</div>)
            text = soup.get_text(separator=' ')
            
            # 3. ZÁKLADNÉ UPRATANIE BIELYCH ZNAKOV
            # Nahradíme viacnásobné medzery a nové riadky jednou medzerou
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Uložíme len ak to má nejakú dĺžku (aspoň 200 znakov)
            if len(text) > 200:
                f_out.write(f"### SOURCE: {url}\n")
                f_out.write(text + "\n\n")
                count += 1
                if count % 500 == 0:
                    print(f"Spracovaných {count} článkov...")

    print(f"Hotovo! Extrahovaných {count} medicínskych textov do {output_file}.")

if __name__ == "__main__":
    simple_extractor("Raw_Clean_Med_Data.txt", "Core_Medical_Text.txt")