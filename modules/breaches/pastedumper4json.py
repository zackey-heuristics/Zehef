import random

from bs4 import BeautifulSoup
from lib.Requests import Request
from lib.colors import *

from .pastedumper import Pastebin_Dumper


class PastebinDumper4JSON(Pastebin_Dumper):
    async def google_dorks_scraper(self):
        r = await Request(f"https://www.google.com/search?q={self.dork}", headers={"User-Agent": random.choice(self.ua)}).get()

        soup = BeautifulSoup(r.text, 'html.parser')
        search_results = soup.find_all('div', class_='tF2Cxc')

        for result in search_results:
            link = result.find('a')['href']

            self.links.append(link)
        
        return self.links

    async def paste_check(self):
        await self.google_dorks_scraper()
        found_pastes = []

        for link in self.links:
            link_raw = link.replace('https://pastebin.com/', 'https://pastebin.com/raw/')
            r = await Request(link_raw).get()

            if self.target.lower() in r.text.lower():
                found_pastes.append(link)

        return found_pastes