from YouTubeChannelAnalyzer.config.configuration import ConfigurationManager
import pandas as pd




class ExploratoryDataAnalysis:

    def __init__(self, config : ConfigurationManager):
        self.config = config

    def data_analysis(self):
        try:
            # Fetch the data
            df_data = pd.read_csv(self.config.data_dir + "Raw_Youtube_API_DATA.csv")
            df_data['total_views'] = pd.to_numeric(df_data['total_views'], errors="coerce")
            df_data['total_likes'] = pd.to_numeric(df_data['total_likes'], errors="coerce")
            df_data['total_comments'] = pd.to_numeric(df_data['total_comments'], errors="coerce")
            df_data['total_subscribers'] = pd.to_numeric(df_data['total_subscribers'], errors="coerce")
            df_data['total_no_of_videos'] = pd.to_numeric(df_data['total_no_of_videos'], errors="coerce")
            df_data['total_no_short_videos'] = pd.to_numeric(df_data['total_no_short_videos'], errors="coerce")
            df_data['total_no_long_videos'] = pd.to_numeric(df_data['total_no_long_videos'], errors="coerce")


            df_data['channel_start_date'] = pd.to_datetime(df_data['channel_start_date'], errors="coerce")
            df_data['inception_date'] = pd.to_datetime(df_data['inception_date'], errors="coerce")

            #check for null values
            # print(df_data.isnull().sum())


            reference_date = pd.to_datetime(pd.Timestamp.now()).tz_localize('UTC')
            # Convert the channel start date and inception date to UTC
            df_data['channel_start_date'] = pd.to_datetime(df_data['channel_start_date']).dt.tz_localize('UTC')
            df_data['inception_date'] = pd.to_datetime(df_data['inception_date']).dt.tz_localize('UTC')
            # Now calculate days since start and inception
            df_data['days_since_start'] = (reference_date - df_data['channel_start_date']).dt.days
            df_data['days_since_inception'] = (reference_date - df_data['inception_date']).dt.days
            final_df = df_data.drop(['channel_id', 'channel_name', 'channel_start_date', 'inception_date'], axis=1)

            final_df.to_csv(self.config.root_dir + "Youtube_channel_data.csv", index= False)
                        
        except Exception as e:
            print(f"An error occurred during model training: {e}")


