import joblib
import pandas as pd
from YouTubeChannelAnalyzer.config.configuration import ConfigurationManager
from YouTubeChannelAnalyzer.logging import logger

class YouTubeSubscriptionPrediction:

    def __init__(self):
        """
        Initialize the class, and load the model training configuration.
        """
        self.config = ConfigurationManager().get_model_training_config()
        self.model = self.load_model()

    def load_model(self):
        """
        Loads the pre-trained model from the saved location.
        :return: Trained model object.
        """
        model_path = self.config.root_dir + "model.pkl"  # Adjust the path if necessary
        try:
            model = joblib.load(model_path)
            logger.info(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Error loading the model: {e}")
            raise

    def predict_subscription_status(self, input_data: dict):
        """
        Predict the subscription status (target variable) for the given input data.
        :param input_data: Dictionary with feature names and values.
        :return: Predicted subscription values.
        """
        try:
            if input_data:
                # Convert the user input dictionary into a DataFrame
                input_df = pd.DataFrame([input_data])

                # Predict using the model
                predicted_values = self.model.predict(input_df)
                logger.info(f"Prediction successful for input data.")
                return predicted_values
            else:
                logger.warning("No valid input data provided!")
                return None
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            raise
