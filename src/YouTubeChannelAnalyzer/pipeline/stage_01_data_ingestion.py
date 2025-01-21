from YouTubeChannelAnalyzer.config.configuration import ConfigurationManager, MongoDBStorage
from YouTubeChannelAnalyzer.conponents.data_ingestion import DataIngestion
from YouTubeChannelAnalyzer.logging import logger
from googleapiclient.discovery import build



class DataIngestionTrainingPipeline:
    def __init__(self, user_input = None):
        self.user_input = user_input
        pass

    def main(self):
        config_manager = ConfigurationManager()
        # Get necessary configurations from .env
        api_key = config_manager.get_youtube_api_key()  # Raises error if not found
        db_connection_string = config_manager.get_mongodb_connection()  # This should work if MONGODB_URI is in the env

        # Initialize MongoDBStorage with the correct URI
        db_storage = MongoDBStorage(db_connection_string)

        # Create DataIngestionConfig using the config manager
        data_ingestion_config = config_manager.get_data_ingestion_config()

        # Initialize the YouTube API client
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Initialize DataIngestion with the correct arguments
        ingestion = DataIngestion(config=data_ingestion_config, youtube=youtube, db_storage=db_storage)

        # Get user input (either channel ID or video URL)
        # user_input = input("Please enter the YouTube video URL or Channel ID: ")

        # Process the user input and begin scraping
        ingestion.process_user_input(self.user_input)  # Pass start_date as well



