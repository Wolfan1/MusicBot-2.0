from pytube import Search
from pytube import YouTube
from http.client import IncompleteRead
from googleapiclient.discovery import build
import youtube_dl
import os

class Song:
    def __init__(self, title, url, success=True):
        self.title = title
        self.url = url
        self.success = success

def search_videos(query, max_results=1):
    # Create a new client object for the YouTube Data API v3
    api_key = os.environ.get("DOJO_REVAMPED_YOUTUBE_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    # Call the search.list method to retrieve search results
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        maxResults=max_results
    ).execute()

    # Extract the video IDs from the search results
    video_ids = [item["id"]["videoId"] for item in search_response["items"]]

    # Call the videos.list method to retrieve video details
    videos_response = youtube.videos().list(
        id=",".join(video_ids),
        part="id,snippet",
        fields="items(id,snippet(title))"
    ).execute()

    # Extract the video titles and URLs from the video details
    video_titles = [item["snippet"]["title"] for item in videos_response["items"]]
    video_urls = ["https://www.youtube.com/watch?v=" + item["id"] for item in videos_response["items"]]

    # Return a list of dictionaries containing video titles and URLs
    return [{"title": title, "url": url} for title, url in zip(video_titles, video_urls)]

def get_audio_stream(query):
    
    youtube_service = os.environ.get('YT_SERVICE')
    
    if youtube_service == 'YTDL':
        # ================
        # Using youtube_dl
        # Doesn't work because of internal youtube changes
        # ================
        
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "prefer_ffmpeg": True,
            "extractaudio": True,
            "audioformat": "mp3",
            "outtmpl": "%(id)s.%(ext)s",
        }

        top_result = search_videos(query)

        # Create youtube_dl object
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # Extract info from video url
            info_dict = ydl.extract_info(top_result[0]["url"], download=False)
            
            # Get the best audio stream URL
            audio_url = info_dict["formats"][0]["url"]
            title = top_result[0]["title"]
        return Song(title, audio_url)
        

    elif youtube_service == 'PYTUBE':

        # ================
        # Using PyTube
        # ================
        while True:
            retries = 3
            try:
                top_result = search_videos(query)
                yt = YouTube(top_result[0]["url"])

                title = top_result[0]["title"]
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_url = audio_stream.url

                return Song(title, audio_url)
            
            except:
                retries -= 1
                if retries == 0:
                    return Song(None, None, success=False)
                else:
                    continue
        


if __name__ == "__main__":

    title, url = get_audio_stream("mo bamba")

    print(f"{title}\n{url}")