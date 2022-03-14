import requests
from bs4 import BeautifulSoup

YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

response = requests.get(YOUTUBE_TRENDING_URL)
print("Response status code: ", response.status_code)

doc = BeautifulSoup(response.text, "html.parser")
video_divs = doc.find_all("div", class_="ytd-video-renderer")
print(f"Number of videos: {len(video_divs)}")