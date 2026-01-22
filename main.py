import requests
import cloudscraper
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Create output PATH if not exists
if not os.path.exists('./output/'):
    os.makedirs('./output/')

load_dotenv() # load .env file (not used)

search_url = "https://vocaloid.fandom.com/api.php"

# song_name = input('Song Name: ')
song_name = "antenna 39"

params = {
    "action": "opensearch",
    "search": song_name,
    "limit": 1,
    "format": "json"
}

# Use cloudscraper to bypass cloudflare
scraper = cloudscraper.create_scraper()

# result format: ['SEARCH_PARAM', ['SONG_NAME_FOUND'], [''], ['WIKI_SONG_URL']
search_result = scraper.get(search_url, params=params)

if search_result.status_code != 200: # Handle Errors
    print("[오류] 검색에 실패했습니다!")
    exit()
wiki_doc_name = search_result.json()[1][0]
print(f"[검색 성공] 곡 이름: {wiki_doc_name}")
url = search_result.json()[3][0] # Target Song URL
response = scraper.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.select(".mw-parser-output table")

    lyrics_table = None

    for table in tables:
        headers = table.select("th")
        for header in headers:
            if header.text.find("Japanese") != -1:
                lyrics_table = table
                break
        if lyrics_table:
            break

    # print(lyrics)

    rows = lyrics_table.find_all("tr")
    # print(rows)

    lyrics_types = rows[0].select("th")
    lyrics_type_string = []
    for lyrics_type in lyrics_types:
        lyrics_type_string.append(lyrics_type.text.strip())

    rows = rows[1:]

    if not os.path.exists(f"./output/{wiki_doc_name}"):
        os.makedirs(f"./output/{wiki_doc_name}")

    for i in range(len(lyrics_type_string)):
        print(lyrics_type_string[i] + '\n')
        with open(f"./output/{wiki_doc_name}/{lyrics_type_string[i].strip()}.txt", "w", encoding="utf-8") as f:
            for row in rows:
                td = row.find_all("td")
                if len(td) > i:
                    f.write(td[i].text.strip() + '\n')
                else:
                    f.write(td[0].text.strip() + '\n')


else:
    print(f"[ERROR CODE: {response.status_code}] Could not fetch from given url...")