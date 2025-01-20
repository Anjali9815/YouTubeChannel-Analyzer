from YouTubeChannelAnalyzer.config.configuration import ConfigurationManager
from YouTubeChannelAnalyzer.conponents.model_trainer import ModelTraining

class ModelTrainingPipeline:
    def __init__(self):
        pass


    def main(self):
        try:
            config_manager = ConfigurationManager()
            modeltraining_config = config_manager.get_model_training_config()
            model_training = ModelTraining(config = modeltraining_config)
            model_training.model_training()
        except Exception as e:
            print(f"An error occurred: {e}")

