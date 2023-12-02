import os
from youtube_fetcher import YoutubeFetcher


def main():
    # Run
    client_youtube = YoutubeFetcher(api_key=os.getenv('YOUTUBE_API_KEY'))
    client_youtube.run_audiobook(query='аудиокнига шлинк')


if __name__ == "__main__":
    main()
