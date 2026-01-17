import requests
import cloudscraper
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

search_url = "https://vocaloid.fandom.com/api.php"

# song_name = input('Song Name: ')
song_name = "antenna"

load_dotenv()

params = {
    "action": "opensearch",
    "search": song_name,
    "limit": 1,
    "format": "json"
}

scraper = cloudscraper.create_scraper()

print(f"[검색 중...] {song_name}")
search_result = scraper.get(search_url, params=params)
if search_result.status_code != 200:
    print("[오류] 검색에 실패했습니다!")
    exit()
print(f"[검색 성공] 곡 이름: {search_result.json()[1][0]}")
url = search_result.json()[3][0]

print(url)

response = scraper.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    lyrics = soup.select(".mw-parser-output table")

    if len(lyrics) >= 4:
        lyrics = lyrics[3].select("td")

    lyrics_parsed = [line.text.strip() for line in lyrics]

    with open(f"./output/{song_name}.txt", "w", encoding="utf-8") as f:
        for line in lyrics_parsed:
            f.write(line + '\n')


else:
    print(f"[ERROR CODE: {response.status_code}]Could not fetch from given url...")