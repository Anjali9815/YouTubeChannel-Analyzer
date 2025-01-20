from YouTubeChannelAnalyzer.entity import DataIngestionConfig
from YouTubeChannelAnalyzer.config.configuration import MongoDBStorage
from YouTubeChannelAnalyzer.logging import logger
from datetime import datetime, timezone
from googleapiclient.discovery import build
import isodate
import pandas as pd
from pymongo import MongoClient
import certifi, re


class DataIngestion:

    def __init__(self, config: DataIngestionConfig, youtube, db_storage: MongoDBStorage):
        """
        Initialize the DataIngestion class with YouTube API client and MongoDB storage.
        :param youtube: YouTube API client.
        :param db_storage: Instance of MongoDBStorage for inserting/updating data.
        """
        self.config = config
        self.youtube = youtube  # YouTube API client
        self.db_storage = db_storage  # MongoDBStorage instance

    def mongo_connect(self, connection_string, db_name='Project1'):
        try:
            client = MongoClient(connection_string, tls=True, tlsCAFile=certifi.where())
            self.db = client[db_name]
            print("Connected")
            logger.info(f"Successfully connected to MongoDB database: {db_name}")
            return self.db
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def close_connection(self):
        if self.db:
            self.db.client.close()
            logger.info("MongoDB connection closed.")

    def youtube_api(self, apikey):
        try:
            self.youtube = build('youtube', 'v3', developerKey=apikey)
            logger.info(f"Youtube Api Configured successfully")
        except:
            logger.info(f"YouTube api not configured")  

    def is_valid_video_url(self, video_url):
        """
        Check if the provided URL is a valid YouTube video URL.
        :param video_url: YouTube video URL.
        :return: Boolean indicating if the URL is valid.
        """
        pattern = r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/(?:[^/]+/|(?:v|e(?:mbed)?)/|watch\?v=)([A-Za-z0-9_-]{11})'
        # print(bool(re.match(pattern, video_url)))
        return bool(re.match(pattern, video_url))

    def get_channel_id_from_video_url(self, video_url):
        try:
            print("***********************")
            video_id_match = re.search(r'(?:youtu.be\/|youtube.com\/(?:v|e(?:mbed)?)\/|youtube.com\/watch\?v=)([a-zA-Z0-9_-]{11})', video_url)
            if video_id_match:
                video_id = video_id_match.group(1)
                logger.info(f"Video ID extracted: {video_id}")
                
                request = self.youtube.videos().list(part="snippet", id=video_id)
                response = request.execute()

                if 'items' in response and len(response['items']) > 0:
                    channel_id = response['items'][0]['snippet']['channelId']
                    logger.info(f"Channel ID for the video is: {channel_id}")
                    print("chanelliddddddd", channel_id)
                    return channel_id
                else:
                    logger.warning("No channel found for this video.")
            else:
                logger.error("Invalid YouTube video URL.")
                return None
        except Exception as e:
            logger.error(f"An error occurred while fetching the channel ID: {e}")
            return None

    def process_user_input(self, user_input):
        """
        Determine whether the user input is a channel ID or a video URL.
        If it's a video URL, extract the channel ID from it.
        :param user_input: User input (channel ID or video URL).
        :param start_date: Start date to filter videos (default is "2025-01-01").
        """
        if self.is_valid_video_url(user_input):
            logger.info("Input is a YouTube Video URL.")
            channel_id = self.get_channel_id_from_video_url(user_input)
            if channel_id:
                logger.info(f"Extracted channel ID: {channel_id}")
                self.get_channel_statistics(channel_id, self.youtube, self.db_storage.db)  # Call the scraping method
            else:
                logger.warning("No channel ID could be extracted from the video URL.")
        else:
            logger.info("Input is a Channel ID.")
            self.get_channel_statistics(user_input, self.youtube, self.db_storage.db)  # Directly use the channel ID


    def parse_duration_to_seconds(self, duration):
        try:
            duration = isodate.parse_duration(duration)
            return int(duration.total_seconds())
        except Exception as e:
            print(f'Error parsing duration {duration}: {e}')
            return 0

    def get_video_statistics(self, video_id):
        try:
            video_response = self.youtube.videos().list(part='statistics,contentDetails', id=video_id).execute()
            video_info = video_response.get('items', [])[0] if 'items' in video_response else {}
            stats = video_info.get('statistics', {})
            details = video_info.get('contentDetails', {})
            
            likes = int(stats.get('likeCount', 0))
            comments = int(stats.get('commentCount', 0))
            duration = details.get('duration', 'PT0S')
            duration_seconds = self.parse_duration_to_seconds(duration)
            
            return likes, comments, duration_seconds
        except Exception as e:
            print(f'Error fetching video data for ID {video_id}: {e}')
            return 0, 0, 0


    def get_channel_statistics(self, channel_id, youtube, db):
        try:
            user_input = '2022-12-01'
            start_date = datetime.strptime(user_input, '%Y-%m-%d').replace(tzinfo=timezone.utc) if user_input else None
            existing_channel = db['youtube_channel_data'].find_one({'channel_id': channel_id})

            if existing_channel:
                print(f"Channel ID {channel_id} already exists. Skipping data fetch.")
                return  # Skip fetching data if it already exists

            channel_response = youtube.channels().list(part='snippet,contentDetails,statistics', id=channel_id).execute()
            logger.info(f"Channel Response: {channel_response}")  # Add this line for debugging

            channel_info = channel_response.get('items', [])[0] if 'items' in channel_response else {}
            
            # if channel_info:
            #     snippet = channel_info.get('snippet', {})
            #     statistics = channel_info.get('statistics', {})
            #     content_details = channel_info.get('contentDetails', {})
            if channel_info:
                snippet = channel_info.get('snippet', {})
                statistics = channel_info.get('statistics', {})
                content_details = channel_info.get('contentDetails', {})
                
                # Fetch channel start date
                channel_start_date = snippet.get('publishedAt', 'NA')
                channel_start_date = datetime.fromisoformat(channel_start_date.replace('Z', '+00:00'))
                
                # Use the user start date for filtering
                # start_date = user_start_date if user_start_date else channel_start_date
                # start_date = channel_start_date
                # Get upload playlist ID
                uploads_playlist_id = content_details.get('relatedPlaylists', {}).get('uploads', 'NA')
                
                if uploads_playlist_id == 'NA':
                    print(f'No uploads playlist found for channel ID {channel_id}.')
                    return
                
                total_likes = 0
                total_comments = 0
                short_videos_count = 0
                long_videos_count = 0
                
                next_page_token = None
                while True:
                    playlist_items_response = youtube.playlistItems().list(
                        part='contentDetails,snippet',
                        playlistId=uploads_playlist_id,
                        maxResults=50,
                        pageToken=next_page_token
                    ).execute()
                    
                    items = playlist_items_response.get('items', [])
                    for item in items:
                        video_id = item['contentDetails']['videoId']
                        video_upload_date = item['snippet'].get('publishedAt', 'NA')
                        video_upload_date = datetime.fromisoformat(video_upload_date.replace('Z', '+00:00'))
                        
                        if video_upload_date >= start_date:
                            likes, comments, duration_seconds = self.get_video_statistics(video_id)
                            total_likes += likes
                            total_comments += comments
                            if duration_seconds < 60:
                                short_videos_count += 1
                            else:
                                long_videos_count += 1
                    
                    next_page_token = playlist_items_response.get('nextPageToken')
                    if not next_page_token:
                        break
                
                # Define the nested structure
                channel_data = {
                    'channel_id': channel_id,
                    'channel_details': {
                        'channel_name': snippet.get('title', 'NA'),
                        'channel_start_date': channel_start_date.isoformat(),
                        'inception_date' : start_date.isoformat(),
                        'total_no_of_videos': statistics.get('videoCount', 'NA'),
                        'total_no_short_videos': short_videos_count,
                        'total_no_long_videos': long_videos_count,
                        'total_views': statistics.get('viewCount', 'NA'),
                        'total_likes': total_likes,
                        'total_comments': total_comments,
                        'total_subscribers': statistics.get('subscriberCount', 'NA'),

                    }
                }

                self.db_storage.insert_or_update_channel_data('youtube_channel_data', channel_data)
            else:
                logger.warning(f'Channel with ID {channel_id} not found or no data available.')
        except Exception as e:
            logger.error(f"Error fetching channel data for ID {channel_id}: {e}")






