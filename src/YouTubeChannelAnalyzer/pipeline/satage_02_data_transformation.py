from YouTubeChannelAnalyzer.config.configuration import ConfigurationManager, MongoDBStorage
from YouTubeChannelAnalyzer.conponents.data_transformation import DataTrasformation



class DataTransformationTrainingPipeline:

    def __init__(self):
        pass

    def main(self):

        config_manager = ConfigurationManager()
        # Get necessary configurations from .env
        api_key = config_manager.get_youtube_api_key()  # Raises error if not found
        db_connection_string = config_manager.get_mongodb_connection()  # This should work if MONGODB_URI is in the env

        # Initialize MongoDBStorage with the correct URI
        db_storage = MongoDBStorage(db_connection_string)

        # Create DataIngestionConfig using the config manager
        data_transformation_config = config_manager.get_data_transformation_config()


        # Initialize DataIngestion with the correct arguments
        data_transformation = DataTrasformation(config=data_transformation_config, db_storage=db_storage)
        data_transformation.data_processing()



