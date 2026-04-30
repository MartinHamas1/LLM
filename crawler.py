import os
import redis
import requests
import threading
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

class HybridMedicalCrawler:
    def __init__(self, max_workers=8):
        self.output_file = "Raw_Clean_Med_Data.txt"
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.lock = threading.Lock()
        self.headers = {
            "User-Agent": "Medical_Research_Bot_v2.4"
        }
        self.allowed_domains = ["www.adc.sk", "www.wikiskripta.eu"]
        self.max_workers = max_workers
        self.data_limit_mb = 3000 

    def is_navigational_junk(self, url):
        junk_patterns = [
            r"Speci", r"Diskuse", r"Redaktor", r"N%C3%A1pov%C4%9Bda", r"Nápověda", 
            r"Kategorie", r"F%C3%B3rum", r"Fórum", r"WikiV", r"Port%C3%A1l", 
            r"Portál", r"Odkaz", r"Soubor", r"Template", r"Šablona", r"WikiThon",
            r"N%C3%A1st%C4%9Bnka", r"Nástěnka", r"Koment%C3%A1%C5%99", r"Komentář",
            r"action=", r"oldid=", r"diff=", r"printable=", r"redirect=", r"limit="
        ]
        return any(re.search(p, url, re.I) for p in junk_patterns)

    def should_save(self, url):
        if self.is_navigational_junk(url):
            return False
            
        if "wikiskripta.eu/w/" in url:
            article_part = url.split("/w/")[-1]
            bad_exact = ["home", "hlavní_strana", "main_page", "index.php", "sandbox"]
            if article_part.lower() in bad_exact:
                return False
            if "._wv" in article_part.lower() or article_part.lower().endswith(".wv"):
                return False
            if ":" in article_part or "/" in article_part or "?" in article_part:
                return False
            if len(article_part) < 3:
                return False
            return True

        if any(x in url for x in ["/detail/", "/pil/", "/spc/"]):
            return True
        
        return False

    def is_allowed_domain(self, url):
        return urlparse(url).netloc in self.allowed_domains

    def save_raw_data(self, url, html):
        with self.lock:
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(f"=== URL: {url} | TYPE: CLEAN_MED ===\n")
                f.write(html)
                f.write("\n=== END ===\n\n")
                f.flush()

    def process_url(self, url):
        if self.r.sadd("visited_urls", url) == 0:
            return

        try:
            time.sleep(0.2)
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code != 200:
                return

            soup = BeautifulSoup(response.text, "html.parser")
            
            for a in soup.find_all('a', href=True):
                link = urljoin(url, a['href']).split('#')[0]
                if self.is_allowed_domain(link) and not self.r.sismember("visited_urls", link):
                    self.r.lpush("crawl_queue", link)

            if self.should_save(url):
                self.save_raw_data(url, response.text)
                print(f" [+] SAVED: {url}")
            else:
                print(f" [.] EXPLORED: {url}")

        except Exception as e:
            print(f" [!] Error {url}: {e}")

    def run(self, seed_urls):
        for seed in seed_urls:
            if not self.r.sismember("visited_urls", seed):
                self.r.lpush("crawl_queue", seed)

        print(f"Crawler 2.4 running. Workers: {self.max_workers}")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            try:
                while True:
                    if os.path.exists(self.output_file) and (os.path.getsize(self.output_file) / (1024**2)) >= self.data_limit_mb:
                        break

                    url = self.r.rpop("crawl_queue")
                    if not url:
                        time.sleep(0)
                        if self.r.llen("crawl_queue") == 0: break
                        continue
                    
                    executor.submit(self.process_url, url)
            except KeyboardInterrupt:
                executor.shutdown(wait=False, cancel_futures=True)
                os._exit(0)

if __name__ == "__main__":
    seeds = [
        "https://www.adc.sk/databazy/produkty.html",
        "https://www.wikiskripta.eu/w/Port%C3%A1l:Medic%C3%ADna",
        "https://www.wikiskripta.eu/w/Speci%C3%A1ln%C3%AD:V%C5%A1echny_str%C3%A1nky"
    ]
    
    crawler = HybridMedicalCrawler(max_workers=60)
    crawler.run(seeds)