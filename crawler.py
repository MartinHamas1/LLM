import asyncio
import redis
import random
import sys
import os
import urllib.parse
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

class MultiSourceMedicalCrawler:
    def __init__(self, seed_urls, redis_host='localhost', max_workers=60):

        self.seed_urls = seed_urls

        self.REDIS_QUEUE = "medical_queue:global"
        self.REDIS_VISITED = "medical_visited:global"
        self.output_file = "Raw_Med_Data.txt"
        self.max_workers = max_workers

        self.allowed_domains = [urlparse(u).netloc for u in seed_urls]
        
        try:
            self.r = redis.Redis(
                host=redis_host, port=6379, db=0, 
                decode_responses=True, socket_timeout=60
            )
            self.r.ping()
            print(f"--- [OK] Pripojené k Redisu. Celkový počet videných: {self.r.scard(self.REDIS_VISITED)} ---")
        except Exception as e:
            print(f"--- [CHYBA] Redis nedostupný: {e} ---")
            sys.exit(1)

        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]

    async def worker(self, browser):
        while True:
            url = self.r.rpop(self.REDIS_QUEUE)
            if not url:
                await asyncio.sleep(5)
                continue

            if self.r.sismember(self.REDIS_VISITED, url):
                continue

            context = await browser.new_context(user_agent=random.choice(self.user_agents))
            page = await context.new_page()
            
            try:
                await page.route("**/*.{png,jpg,jpeg,svg,mp4,mp3,woff,woff2,css}", lambda route: route.abort())
                
                print(f"Sťahujem: {url}")
                await page.goto(url, timeout=45000, wait_until="domcontentloaded")
                
                raw_html = await page.content()

                with open(self.output_file, "a", encoding="utf-8") as f:
                    f.write(f"\n\n=== SOURCE_START URL: {url} ===\n")
                    f.write(raw_html)
                    f.write(f"\n=== SOURCE_END URL: {url} ===\n")
                
                self.r.sadd(self.REDIS_VISITED, url)

                soup = BeautifulSoup(raw_html, 'html.parser')
                for a in soup.find_all('a', href=True):
                    full_url = urllib.parse.urljoin(url, a['href']).split('#')[0].rstrip('/')
                    parsed_url = urlparse(full_url)

                    if parsed_url.netloc in self.allowed_domains:
                        decoded_url = urllib.parse.unquote(full_url).lower()
                        odpad = ['index.php', 'action=', 'diff=', 'oldid=', 'search=', 'special:', 'kategorie:', 'soubor:']
                        
                        if any(x in decoded_url for x in odpad):
                            continue

                        if not self.r.sismember(self.REDIS_VISITED, full_url):
                            self.r.lpush(self.REDIS_QUEUE, full_url)

            except Exception as e:
                pass 
            finally:
                await page.close()
                await context.close()
            
            await asyncio.sleep(random.uniform(0.5, 1.5))

    async def run(self):
        if self.r.llen(self.REDIS_QUEUE) == 0:
            for s_url in self.seed_urls:
                self.r.lpush(self.REDIS_QUEUE, s_url)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            await asyncio.gather(*[self.worker(browser) for _ in range(self.max_workers)])
            await browser.close()

if __name__ == "__main__":
    targets = [
        "https://www.wikiskripta.eu",
        "https://www.nzip.cz",            
        "https://www.stefajir.cz",         
        "https://www.ordinace.cz",         
        "https://www.zdravie.sk",          
        "https://sk.wikipedia.org/wiki/Kategória:Medicína", 
        "https://cs.wikipedia.org/wiki/Portál:Medicína"    
    ]
    
    crawler = MultiSourceMedicalCrawler(targets, max_workers=60) 
    
    try:
        asyncio.run(crawler.run())
    except KeyboardInterrupt:
        print("\n--- Zastavené. ---")