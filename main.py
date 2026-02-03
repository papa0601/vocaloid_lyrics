import requests
import cloudscraper
from bs4 import BeautifulSoup
import os
import json

def make_local_cache(html, filename):
    with open(f"./{filename}.html", "w", encoding="utf-8") as f:
        f.writelines(html)

def load_local_cache(filename) -> str:
    with open(f"./{filename}.html", "r", encoding="utf-8") as f:
        return f.readlines() 

scraper = cloudscraper.create_scraper()
search_url = "https://vocaloidlyrics.miraheze.org/w/api.php" # 검색할 위키의 엔드포인트
song_name = "antenna" # 검색어
params = {
    "action": "opensearch",
    "search": song_name,
    "limit": 7,
    "format": "json"
}
SEARCH_TARGET_EXCEPTION = ("disambiguation", "album")
search_result = scraper.get(search_url, params=params)
# Search Result 형식: ['검색어'], [검색된 문서의 풀네임], [정체 불명의 빈 리스트], [검색된 문서의 링크]]

if search_result.status_code != 200:
    raise(Exception("[오류] 검색에 실패했습니다!"))

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

if not all((song_document_name, song_document_link)):
    raise(Exception("[오류] 검색은 완료했으나, 노래를 찾을 수 없습니다!"))

print(f"[검색 성공] 문서 제목: {song_document_name} (링크: {song_document_link})")

response = scraper.get(song_document_link)
if response.status_code != 200:
    raise(Exception("[오류] 검색한 문서를 불러오지 못했습니다!"))

html = response.text
soup = BeautifulSoup(html, 'html.parser')



