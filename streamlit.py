import streamlit as st
import logging
from main import train_model  # Importing the function from trainer.py
from time import sleep  # To simulate the delay during model training

# Assuming YouTubeSubscriptionPrediction is the class that provides the prediction logic
from YouTubeChannelAnalyzer.pipeline.predict import YouTubeSubscriptionPrediction  # You can import from your actual model file

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global flag to track if the pipeline is already running
is_pipeline_running = False

# Track the status of the training process
training_status = "Not started"

# Function to simulate background task handling
def run_training_task(run_data_ingestion: bool, user_input: str):
    """
    This function will run the training task.
    """
    try:
        # Check if we need to run data ingestion
        if run_data_ingestion:
            # Run data ingestion logic here (e.g., loading data, preprocessing)
            logger.info("Running data ingestion...")
            # Simulate the data ingestion process (replace this with actual code)
            sleep(2)
        
        # Run the model training (after ingestion, or directly if ingestion is skipped)
        logger.info("Running model training...")
        result = train_model(run_data_ingestion=run_data_ingestion, user_input=user_input)
        
        # Log and return the result
        logger.info(f"Training result: {result}")
        return result

    except Exception as e:
        logger.error(f"Error during training: {e}")
        return str(e)

# Streamlit UI
st.title('Model Training and Prediction Pipeline')

# Display the status
status_container = st.empty()
status_container.text(f"Training Status: {training_status}")

# Model training form
with st.form(key='training_form'):
    channel_info = st.text_input("Enter Channel Info (Optional)", "")
    run_data_ingestion = st.checkbox("Run Data Ingestion", value=False)

    submit_button = st.form_submit_button("Start Training")

if submit_button:
    # Check if training is already running
    if is_pipeline_running:
        st.error("Error: Training pipeline is already running.")
    elif channel_info == "":
        st.warning("Channel Info is empty. Skipping Data Ingestion and continuing with other stages.")
        # Run the training with None or empty channel info
        user_input = None  # Set user_input to None if no channel info is provided
    else:
        user_input = channel_info  # Use the provided channel info as user input
    
    # Update the status to "Training started"
    is_pipeline_running = True
    training_status = "Training started"
    status_container.text(f"Training Status: {training_status}")
    
    # Simulate the background task
    with st.spinner("Training in progress... Please wait."):
        sleep(2)  # Simulate some processing time (replace with actual training logic)
        result = run_training_task(run_data_ingestion, user_input)

    # Display the result
    if isinstance(result, str):  # If an error occurred during training
        training_status = "Error occurred"
        st.error(f"Training failed: {result}")
    else:
        training_status = "Training completed successfully"
        st.success(f"Training completed. Result: {result}")

    # Reset the pipeline status
    is_pipeline_running = False
    status_container.text(f"Training Status: {training_status}")

# Subscription Prediction Form
st.subheader("You can predict subscription status here (optional)")

with st.form(key="prediction_form"):
    total_no_of_videos = st.number_input("Enter the total number of videos:", min_value=0.0)
    total_no_short_videos = st.number_input("Enter the total number of short videos:", min_value=0.0)
    total_no_long_videos = st.number_input("Enter the total number of long videos:", min_value=0.0)
    total_views = st.number_input("Enter the total views:", min_value=0.0)
    total_likes = st.number_input("Enter the total likes:", min_value=0.0)
    total_comments = st.number_input("Enter the total comments:", min_value=0.0)
    days_since_start = st.number_input("Enter the number of days since the channel started:", min_value=0.0)
    days_since_inception = st.number_input("Enter the number of days since the channel inception:", min_value=0.0)

    prediction_submit_button = st.form_submit_button(label="Predict Subscription Status")

if prediction_submit_button:
    input_data = {
        'total_no_of_videos': total_no_of_videos,
        'total_no_short_videos': total_no_short_videos,
        'total_no_long_videos': total_no_long_videos,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'days_since_start': days_since_start,
        'days_since_inception': days_since_inception
    }

    # Prediction logic (using YouTubeSubscriptionPrediction model)
    subscription_predictor = YouTubeSubscriptionPrediction()

    predicted_value = subscription_predictor.predict_subscription_status(input_data)

    if predicted_value is not None:
        predicted_value = predicted_value[0]  # Get the scalar value from the array
        st.write(f"Predicted Subscription Status: {predicted_value:.2f} subscribers")
    else:
        st.error("Prediction failed. Please check the input values.")
