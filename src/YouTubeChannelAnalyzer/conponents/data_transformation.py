from YouTubeChannelAnalyzer.logging import logger
import pandas as pd
from YouTubeChannelAnalyzer.config.configuration import ConfigurationManager, MongoDBStorage


class DataTrasformation():

    def __init__(self, config : ConfigurationManager, db_storage : MongoDBStorage):
        self.config = config
        self.db_storage = db_storage

    def data_processing(self):
        try:
            collection = self.db_storage.db['youtube_channel_data'] 
            # Define the fields to retrieve
            fields = {
                'channel_id': 1,
                'channel_details.channel_name': 1,
                'channel_details.channel_start_date': 1,
                'channel_details.inception_date': 1,
                'channel_details.total_no_of_videos': 1,
                'channel_details.total_no_short_videos': 1,
                'channel_details.total_no_long_videos': 1,
                'channel_details.total_views': 1,
                'channel_details.total_likes': 1,
                'channel_details.total_comments': 1,
                'channel_details.total_subscribers': 1
            }

            # Fetch documents and project the required fields
            documents = collection.find({}, {field: 1 for field in fields})

            # Convert documents to a list of dictionaries
            data = list(documents)

            # Normalize nested data for DataFrame
            df_data = pd.json_normalize(data, sep='_')

            # Rename columns to remove 'channel_details_' prefix
            df_data.columns = df_data.columns.str.replace('channel_details_', '', regex=False)

            # Convert date fields to YYYY-MM-DD format
            date_columns = ['channel_start_date', 'inception_date']
            for column in date_columns:
                # Convert to datetime, handling potential microseconds
                df_data[column] = pd.to_datetime(df_data[column].str.replace(r'\.\d+', '', regex=True)).dt.strftime('%Y-%m-%d')

            # Drop the '_id' column if it exists
            df_data.drop('_id', axis=1, inplace=True, errors='ignore')

            # Save to CSV
            df_data.to_csv(self.config.data_dir + "Raw_Youtube_API_DATA.csv", index=False)
        except Exception as e:
            print(e)
            logger.error(f"Error processing data: {e}")



