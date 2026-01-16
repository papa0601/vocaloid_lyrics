import requests
from bs4 import BeautifulSoup

url = "https://vocaloid.fandom.com/wiki/"

song_name = 'lustrous'

song_name = song_name.replace(' ', '_')

response = requests.get(url + song_name)

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