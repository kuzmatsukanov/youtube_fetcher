import os
import csv
import pandas as pd
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

    def search_video(self, query, duration='any', lang=None, max_results=50, page_token=None,
                     save_next_page_token=True):
        """
        Search for videos.

        Args:
            query (str): The search query.
            duration (str, optional): The video duration
                (e.g., 'any', 'long'(>20min), 'medium'(4-20min), 'short'(<4min)).
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

    @staticmethod
    def _remove_duplicates(input_file, output_file):
        """
        Remove duplicate lines from an input file and save unique lines to an output file.

        Args:
            input_file (str): Path to the input file.
            output_file (str): Path to the output file where unique lines will be saved.
        """
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(input_file)

            # Drop duplicate rows based on all columns
            df_unique = df.drop_duplicates()

            # Save the unique DataFrame to a new CSV file
            df_unique.to_csv(output_file, index=False)
        except FileNotFoundError:
            print(f"File '{input_file}' not found. Please provide a valid file path.")

    @staticmethod
    def _filter_by_word(input_file, output_file, keywords):
        """
        Filter a CSV file based on specified keywords in either the 'title' and 'description' columns (case-insensitive).
        The filtered data is saved to a new CSV file.

        Args:
            input_file (str): Path to the input CSV file.
            output_file (str): Path to save the filtered data as a new CSV file.
            keywords (iterable): List of words to filter by.
        """
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(input_file)

            # Filter rows that contain any of the specified keywords in either of the two columns (case-insensitive)
            filter_condition = (
                    df['title'].str.contains('|'.join(keywords), case=False) |
                    df['description'].str.contains('|'.join(keywords), case=False)
            )
            df_filtered = df[filter_condition]

            # Save the filtered DataFrame to a new CSV file
            df_filtered.to_csv(output_file, index=False)
        except FileNotFoundError:
            print(f"File '{input_file}' not found. Please provide a valid file path.")

    def run_audiobook(self, query, max_pages=3):
        """Run search, save, and filtration for audiobooks"""
        for i in range(max_pages):
            self.search_video(query=query, duration='long', lang='ru', max_results=50)
            self.save_to_csv('audiobooks.csv')
        self._remove_duplicates('audiobooks.csv', 'audiobooks.csv')
        self._filter_by_word('audiobooks.csv', 'audiobooks.csv', ('аудиокниг', 'радиоспектакл'))
