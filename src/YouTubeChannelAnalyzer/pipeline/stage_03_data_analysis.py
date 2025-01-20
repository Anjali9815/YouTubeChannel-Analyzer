from YouTubeChannelAnalyzer.config.configuration import ConfigurationManager
from YouTubeChannelAnalyzer.conponents.data_analysis import ExploratoryDataAnalysis


class DataAnalysisTrainingPipeline:
    
    def __init__(self):
        pass


    def main(self):
        try:
            config_manager = ConfigurationManager()
            eda_config = config_manager.get_dataanalysis_config()
            eda = ExploratoryDataAnalysis(config = eda_config)
            eda.data_analysis()
        except Exception as e:
            print(f"An error occurred: {e}")


