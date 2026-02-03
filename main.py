import requests
import cloudscraper
from bs4 import BeautifulSoup
import os
import json

def make_local_cache(html, filename):
    with open(f"./{filename}.html", "w", encoding="utf-8") as f:
        f.write(html)

def load_local_cache(filename) -> str:
    with open(f"./{filename}.html", "r", encoding="utf-8") as f:
        return ''.join(f.readlines()) 

song_name = "antenna" # 검색어 # TODO 나중에 위치 바꾸셈! 
'''
scraper = cloudscraper.create_scraper()
search_url = "https://vocaloidlyrics.miraheze.org/w/api.php" # 검색할 위키의 엔드포인트
params = {
    "action": "opensearch",
    "search": song_name,
    "limit": 7,
    "format": "json"
}
SEARCH_TARGET_EXCEPTION = ("disambiguation", "album") # 검색 예외 단어 설정
search_result = scraper.get(search_url, params=params)
# search_result의 json 형식: ['검색어', [검색된 문서의 풀네임 리스트], [검색된 문서 수 길이의 빈 리스트], [검색된 문서의 링크 리스트]]

if search_result.status_code != 200:
    raise Exception("[오류] 검색에 실패했습니다!")

search_result_json = search_result.json()
song_document_name = None
song_document_link = None

for i in range(len(search_result_json[1])):
    # 예외 단어가 포함된 검색 결과는 무시합니다.
    if any(ignore_word in search_result_json[1][i] for ignore_word in SEARCH_TARGET_EXCEPTION):
        continue

    song_document_name = search_result_json[1][i]
    song_document_link = search_result_json[3][i]
    break

else:
    raise Exception("[오류] 검색은 완료했으나, 노래를 찾을 수 없습니다!")

print(f"[검색 성공] 문서 제목: {song_document_name} (링크: {song_document_link})")

response = scraper.get(song_document_link)
if response.status_code != 200:
    raise Exception("[오류] 검색한 문서를 불러오지 못했습니다!")

html = response.text

make_local_cache(html, "antenna")
'''
html = load_local_cache("antenna")
soup = BeautifulSoup(html, 'html.parser')

lyrics_table = soup.select_one('[class="lyrics-table"]')
lyrics_type_header = lyrics_table.select_one('[class="lyrics-table-header"]')
lyrics_type_list = tuple(lyrics_type.text.strip() for lyrics_type in lyrics_type_header.select("th"))

lyrics = []
for i in range(len(lyrics_type_list)): lyrics.append([])
lyric_lines = lyrics_table.select("tr")[1:] # 헤더 제외

for lyric_line in lyric_lines:
    part = lyric_line.select("td")
    for idx in range(len(lyrics_type_list)):
        target_text = part[idx].text if len(part) > idx else part[0].text
        target_text = target_text.strip()
        if target_text:
            lyrics[idx].append(target_text)

target_directory = os.path.join(".", "output", song_name)
# output 폴더 만들기
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

for lyric_type, lyric in zip(lyrics_type_list, lyrics):
    with open(os.path.join(target_directory, lyric_type + '.txt'), "w", encoding="utf-8") as f:
        f.write("\n".join(lyric) + "\n")

# TODO 한 노래를 크롤링 하는 과정을 함수로 감싸서 한 번에 여러 노래를 비동기로 처리할 궁리를 해보자! 