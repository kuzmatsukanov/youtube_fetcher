import os
import csv
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()


class YoutubeFetcher:
    def __init__(self, api_key):
        """
        Initialize the YoutubeFetcher object.

        Args:
            api_key (str): The YouTube Data API key.
        """
        self.client_youtube = build('youtube', 'v3', developerKey=api_key)
        self.response = {}

    def search_video(self, query, duration='any', lang=None, max_results=50, page_token=None, save_next_page_token=True):
        """
        Search for videos.

        Args:
            query (str): The search query.
            duration (str, optional): The video duration (e.g., 'any', 'long'(>20min), 'medium'(4-20min), 'short'(<4min)).
            lang (str, optional): The language of the videos, e.g. 'en'.
            max_results (int, optional): Maximum number of results to fetch per request. Allowed values [0, 50].
            page_token (str, optional): Token for pagination. Defaults to None.
            save_next_page_token (bool, optional): Whether to save the next page token to a file. Defaults to True.
        """
        if page_token is None:
            page_token = self.response.get('nextPageToken', None)

        request = self.client_youtube.search().list(
            q=query,
            type='video',
            part='snippet',
            videoDuration=duration,
            relevanceLanguage=lang,
            maxResults=max_results,  # [0, 50]
            safeSearch="none",
            pageToken=page_token,
        )

        try:
            self.response = request.execute()
            if save_next_page_token:
                self._save_page_token()
        except Exception as e:
            print(f"An error occurred: {e}")

    def _save_page_token(self):
        """
        Save the next page token to a file.
        """
        next_page_token = self.response.get('nextPageToken', None)
        if next_page_token:
            with open('page_token.txt', 'a') as file:
                file.write(f"{next_page_token}\n")

    def save_to_csv(self, file_path):
        """
        Save fetched video data to a CSV file.

        Args:
            file_path (str): The path to the CSV file.
        """
        if 'items' in self.response:
            for item in self.response['items']:
                self._save_item_to_csv(item, file_path)
        else:
            print("Nothing is saved. No items were found in the response.")

    @staticmethod
    def _save_item_to_csv(data, file_path):
        """
        Save video item data to a CSV file.

        Args:
            data (dict): Dictionary containing video data.
            file_path (str): The path to the CSV file.
        """
        parameters = {
            'title': data['snippet']['title'],
            'description': data['snippet']['description'],
            'channelTitle': data['snippet']['channelTitle'],
            'channelId': data['snippet']['channelId'],
            'publishedAt': data['snippet']['publishedAt'],
            'default_thumbnail_url': data['snippet']['thumbnails']['default']['url'],
        }

        # Write the extracted parameters to a CSV file
        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=parameters.keys())
            if not os.path.exists(file_path):
                writer.writeheader()
            writer.writerow(parameters)

    def _clear_response(self):
        """
        Clear the stored response from previous searches.
        """
        self.response = {}


# # Run
# clientYoutube = YoutubeFetcher(api_key=os.getenv('YOUTUBE_API_KEY'))
# clientYoutube.search_video(query='Аудиокнига', duration='long', lang='ru', max_results=50)
# clientYoutube.save_to_csv('audiobooks.csv')
