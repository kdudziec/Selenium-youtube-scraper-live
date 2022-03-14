import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  # chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  driver.get(YOUTUBE_TRENDING_URL)
  driver.implicitly_wait(10)
  time.sleep(5)
  videos = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
  return videos

def parse_video(video):
  # scroll down a little
  actions = ActionChains(driver)
  actions.send_keys(Keys.DOWN*4)
  actions.perform()
  # get video's title
  video_title_tag = video.find_element(By.ID, "video-title")
  video_title = video_title_tag.text  
  # get video's url
  video_url = video_title_tag.get_attribute("href")
  thumbnail_tag = video.find_element(By.TAG_NAME, "img")
  #get video's thumbnail
  thumbnail_url = thumbnail_tag.get_attribute("src")
  # get video's channel name
  channel_div = video.find_element(By.CLASS_NAME, "ytd-channel-name")
  channel_name = channel_div.text
  # get video's description
  description = video.find_element(By.ID, "description-text").text
  return {
    "title": video_title,
    "url": video_url,
    "thumbnail_url": thumbnail_url,
    "channel": channel_name,
    "description": description
  }
  

if __name__ == "__main__":
  print("Creating driver")
  driver = get_driver()
  print("Fetching trending videos")
  videos = get_videos(driver)
  print("Parsing Top 10 videos")
  videos_data = [parse_video(video) for video in videos[:10]]
  print(videos_data[1])

  print("Save the data to a CSV")
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  videos_df.to_csv("trending.csv", index=None)
