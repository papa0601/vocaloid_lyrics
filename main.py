import requests
import cloudscraper
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json

# Create output PATH if not exists
if not os.path.exists('./output/'):
    os.makedirs('./output/')

load_dotenv() # load .env file (not used)

search_url = "https://vocaloid.fandom.com/api.php"

# song_name = input('Song Name: ')
song_name = "M@GICAL"

params = {
    "action": "opensearch",
    "search": song_name,
    "limit": 1,
    "format": "json"
}

with open("./blacklist.json", "r", encoding="utf-8") as f:
    blacklist = json.load(f)

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
    
    # 실행하기 전에 이거 확인하셈 ㅇㅇ
    with open("./test.html", "w", encoding="utf-8") as f:
        f.writelines(html)
    exit()
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.select(".mw-parser-output table")
    lyrics_tables_origins = soup.select('[class="wds-tabs__tab-label"]')

    lyrics_table_names = []

    
    # 노래의 여러가지 버전이 존재할 경우 그것들의 이름을 추출합니다
    for lyrics_tables_origin in lyrics_tables_origins:
        print(lyrics_tables_origin)
        if lyrics_tables_origin.text.strip() not in blacklist and lyrics_tables_origin.text.strip().find("Unofficial") == -1:
            lyrics_table_names.append(lyrics_tables_origin.text.strip())
    print(lyrics_table_names)

    if not lyrics_table_names:
        lyrics_table_names.append('Default')


    lyrics_tables = []

    for x in range(len(lyrics_table_names)):
            if not os.path.exists(f"./output/{wiki_doc_name}{'/' + (lyrics_table_names[x]) if len(lyrics_table_names) > 1 else ''}"):
                os.makedirs(f"./output/{wiki_doc_name}{'/' + (lyrics_table_names[x]) if len(lyrics_table_names) > 1 else ''}")

    for table in tables:
        headers = table.select("th")
        for header in headers:
            if header.text.find("Japanese") != -1 or header.text.find("English") != -1:
                lyrics_tables.append(table)
                break
    print(len(lyrics_tables))
    for i, lyrics_table in enumerate(lyrics_tables):

        rows = lyrics_table.find_all("tr")
        lyrics_types = rows[0].select("th")
        lyrics_type_string = []
        for lyrics_type in lyrics_types:
            lyrics_type_string.append(lyrics_type.text.strip())
        rows = rows[1:]

        for j in range(len(lyrics_type_string)):
            print(lyrics_type_string[j] + '\n')
            with open(f"./output/{wiki_doc_name}/{(lyrics_table_names[i] + '/') if len(lyrics_table_names) > 1 else ''}{lyrics_type_string[j].strip().replace(' ', '_')}.txt", "w", encoding="utf-8") as f:
                for row in rows:
                    td = row.find_all("td")
                    if len(td) > j:
                        f.write(td[j].text.strip() + '\n')
                    else:
                        f.write(td[0].text.strip() + '\n')


else:
    print(f"[ERROR CODE: {response.status_code}] Could not fetch from given url...")