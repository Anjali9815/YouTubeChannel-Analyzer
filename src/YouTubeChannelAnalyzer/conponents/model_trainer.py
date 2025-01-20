from YouTubeChannelAnalyzer.config.configuration import ModelTrainerconfig
from YouTubeChannelAnalyzer.logging import logger
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor


class ModelTraining:

    def __init__(self, config: ModelTrainerconfig):
        self.config = config
        self.params = config

    def model_training(self):
        try:
            # Fetch the data (assuming the path in `self.config.data_dir` is valid)
            df_data = pd.read_csv(self.config.data_dir + "Youtube_channel_data.csv")
            logger.info(f"Data loaded from {self.config.data_dir}.")
            # print(df_data)
            
            # # Example: assume df has features and a target column
            # # x = df_data.drop(['channel_id', 'channel_name', 'channel_start_date', 'inception_date', 'total_subscribers'], axis=1)
            # x = df_data[['total_views', 'total_likes', 'total_comments', 'total_no_of_videos', 'total_no_long_videos', 'days_since_start']]
            # y = df_data['total_subscribers']
            x = df_data.drop(columns='total_subscribers', axis= 1)
            y = df_data['total_subscribers']


            # # Split the data into train and test sets
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=self.params.test_size, random_state=self.params.random_state_size)
            logger.info(f"Data split into training and testing sets with test size: {self.params.test_size}.")

            # # Initialize the model (e.g., Random Forest)
            model = RandomForestRegressor(n_estimators=self.params.n_estimators, random_state=self.params.random_state)
            logger.info("Random Forest model initialized.")

            # # Train the model
            model.fit(X_train, y_train)
            logger.info("Model training completed.")

            logger.info(f"Model accuracy: {model.score(X_test, y_test):.2f}")
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            logger.info(f"Model evaluation completed. MAE: {mae:.2f}, MSE: {mse:.2f}, R^2: {r2:.2f}")

            # Save the trained model
            joblib.dump(model, self.config.root_dir + "model.pkl")
            logger.info(f"Model saved to {self.config.root_dir}.")

        except Exception as e:
            logger.error(f"An error occurred during model training: {e}")
            raise




