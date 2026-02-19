from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)

def search_videos(query, max_results=50):
    last_month = (pd.Timestamp.now('UTC') - pd.Timedelta(days=30)).isoformat()
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video", 
        order="viewCount",
        publishedAfter = last_month,
        maxResults = max_results
    )
    response = request.execute()
    video_ids = [item["id"]["videoId"] for item in response["items"]]
    return video_ids

def get_video_details(video_ids):
    all_data = []
    for i in range(0, len(video_ids), 50): 
        request = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids[i:i+50])
        )
        response = request.execute() #returning the JSON response
        for video in response["items"]:
            data = {
                "title": video["snippet"]["title"],
                "published": video["snippet"]["publishedAt"],
                "views": int(video.get("statistics", {}).get("viewCount", 0)),
                "channelTitle": video["snippet"]["channelTitle"]
            }
            all_data.append(data) #merging into a single DataFrame
    return pd.DataFrame(all_data)


def main():
    df = get_video_details(search_videos("Hello Kitty Island Adventure", 50))
    df.to_csv("hkia_youtube_data.csv", index=False)
    print("Data successfully saved to hkia_youtube_data.csv")


if __name__ == "__main__":
    main()