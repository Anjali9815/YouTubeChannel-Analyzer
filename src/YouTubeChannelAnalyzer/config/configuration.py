from YouTubeChannelAnalyzer.constants import *
from YouTubeChannelAnalyzer.utils.common import create_directories, read_yaml
from YouTubeChannelAnalyzer.logging import logger
from datetime import datetime, timezone
from googleapiclient.discovery import build
from pymongo import MongoClient
import certifi, os
from YouTubeChannelAnalyzer.entity import DataIngestionConfig


class ConfigurationManager():
    def __init__(self, config_filepath = CONFIG_FILE_PATH, params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        # Create necessary directories
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Retrieves the data ingestion configuration from the YAML file and creates necessary directories.
        """
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        return DataIngestionConfig(root_dir=config.root_dir)

    def get_youtube_api_key(self) -> str:
        """
        Retrieves the YouTube API key from environment variables.
        If missing, logs an error and raises an exception.
        """
        youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        youtube_api_key = "AIzaSyBPJ64uexibg77DCSd6rSGU8loyOTvndjI"
        if not youtube_api_key:
            logger.error("YouTube API key is missing from the environment variables.")
            raise ValueError("YouTube API key is missing from environment variables.")
        return youtube_api_key

    def get_mongodb_connection(self) -> str:
        """
        Retrieves the MongoDB connection string from environment variables.
        If missing, logs an error and raises an exception.
        """
        mongodb_uri = os.getenv('MONGODB_URI')
        mongodb_uri = "mongodb+srv://anjalijha1507:U54OU4PFxPYlVc4S@youtubedata.shzzp.mongodb.net/?retryWrites=true&w=majority&appName=YoutubeData"
        if not mongodb_uri:
            logger.error("MongoDB URI is missing from the environment variables.")
            raise ValueError("MongoDB URI is missing from environment variables.")
        return mongodb_uri

    def get_start_date(self, user_input_date: str = None) -> datetime:
        """
        Retrieves the start date either from user input or environment variables.
        If not provided, defaults to '2025-01-01'.
        """
        default_start_date = '2025-01-01'
        
        if user_input_date:
            try:
                start_date = datetime.strptime(user_input_date, '%Y-%m-%d')
                return start_date
            except ValueError:
                logger.error("Invalid start date format provided. Using default start date.")
                return datetime.strptime(default_start_date, '%Y-%m-%d')
        
        return datetime.strptime(default_start_date, '%Y-%m-%d')


class MongoDBStorage:
    def __init__(self, connection_string, db_name='Project1'):
        """
        Initialize the MongoDB storage handler.
        :param connection_string: MongoDB connection string.
        :param db_name: MongoDB database name (default is 'Project1').
        """
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """
        Establish a connection to MongoDB.
        """
        try:
            self.client = MongoClient(self.connection_string, tls=True, tlsCAFile=certifi.where())
            self.db = self.client[self.db_name]
            logger.info(f"MongoDB connection successful. Connected to database: {self.db_name}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def insert_or_update_channel_data(self, collection_name, channel_data):
        """
        Insert or update the channel data in the specified collection.
        :param collection_name: Name of the MongoDB collection.
        :param channel_data: The channel data to be inserted or updated.
        """
        try:
            collection = self.db[collection_name]
            # Use the 'channel_id' as the unique identifier for the update operation
            collection.update_one(
                {'channel_id': channel_data['channel_id']},
                {'$set': channel_data},
                upsert=True
            )
            logger.info(f"Data for channel {channel_data['channel_id']} successfully inserted/updated.")
        except Exception as e:
            logger.error(f"Failed to insert/update channel data: {e}")
            raise

    def close(self):
        """
        Close the MongoDB connection when done.
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")



