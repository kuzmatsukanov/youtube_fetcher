# YouTube Data API Fetcher

This Python class, `YoutubeFetcher`, allows users to interact with the YouTube Data API to search for videos based on various criteria and save the fetched video data to a CSV file.

## Installation

1. Clone the repository.
2. Install the required dependencies: `pip install -r requirements.txt`
3. To use this class, you'll need a YouTube Data API key. You can obtain it by following the instructions in the [YouTube API documentation](https://developers.google.com/youtube/v3/getting-started).


## Usage

1. Create an instance of `YoutubeFetcher` by providing your YouTube Data API key:

    ```python
    from youtube_fetcher import YoutubeFetcher

    api_key = 'YOUR_API_KEY'
    youtube_fetcher = YoutubeFetcher(api_key)
    ```

2. Search for videos:

    ```python
    # Search for Russian audiobooks more than 20 minutes in duration
    youtube_fetcher.search_video(query='Аудиокнига', duration='long', lang='ru', max_results=50)
    ```

3. Save fetched video data to a CSV file:

    ```python
    # Save fetched data to a CSV file
    youtube_fetcher.save_to_csv('video_data.csv')
    ```

## Parameters

- `query`: The search query for videos.
- `duration`: The duration of videos to search for ('any', 'long', 'medium', 'short').
- `lang`: The language of the videos.
- `max_results`: Maximum number of results to fetch per request (0 to 50).