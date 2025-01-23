from fastapi import FastAPI, BackgroundTasks, Query, Response
from main import train_model  # Importing the function from trainer.py
import logging
from YouTubeChannelAnalyzer.pipeline.predict import YouTubeSubscriptionPrediction  # You can import from your actual model file
from fastapi import FastAPI
import uvicorn
# FastAPI instance
app = FastAPI()

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global flag to track if the pipeline is already running
is_pipeline_running = False

# Track the status of the training process
training_status = "Not started"

# Background task to handle model training
def run_training_task(run_data_ingestion: bool, user_input: str):
    """
    This function will run the training task.
    """
    try:
        # Calling the train_model function from trainer.py to start the training
        result = train_model(run_data_ingestion=run_data_ingestion, user_input=user_input)
        logger.info(f"Training result: {result}")

    except Exception as e:
        logger.error(f"Error during training: {e}")

# API endpoint to trigger the training process
@app.get("/train")
async def training(background_tasks: BackgroundTasks, 
                   run_data_ingestion: bool = Query(False), 
                   channel_info: str = Query(...)):
    """
    This endpoint starts the training process.
    It will only run once unless manually triggered again.
    """
    global is_pipeline_running, training_status

    # Check if the pipeline is already running
    if is_pipeline_running:
        return Response("Error: Training pipeline is already running.", status_code=400)

    # Validate if the channel_info is provided
    if not channel_info:
        return Response("Error: channel_info parameter cannot be empty.", status_code=400)

    try:
        # Set the flag to indicate that the pipeline is running
        is_pipeline_running = True
        training_status = "Training started"

        # Add the background task for training
        background_tasks.add_task(run_training_task, run_data_ingestion, channel_info)
        # print("******************///////")
        result = train_model(run_data_ingestion=run_data_ingestion, user_input=channel_info)

        # Return the status from train_model after it completes
        return result


        # Response indicating the training has started
        return {"status": "Training started in the background."}

    except Exception as e:
        # Reset the flag in case of error
        is_pipeline_running = False
        training_status = "Error occurred"
        return Response(f"Error occurred: {e}", status_code=500)




# API endpoint for making predictions
@app.get("/predict")
async def predict_subscription_status(total_no_of_videos: float = Query(...),
                                       total_no_short_videos: float = Query(...),
                                       total_no_long_videos: float = Query(...),
                                       total_views: float = Query(...),
                                       total_likes: float = Query(...),
                                       total_comments: float = Query(...),
                                       days_since_start: float = Query(...),
                                       days_since_inception: float = Query(...)):
    """
    This endpoint makes a prediction for the YouTube subscription status.
    It receives input parameters and uses the YouTubeSubscriptionPrediction model to predict.
    """
    # Prepare the input data for prediction
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

    # Initialize the prediction model
    subscription_predictor = YouTubeSubscriptionPrediction()

    try:
        # Predict the subscription status
        predicted_value = subscription_predictor.predict_subscription_status(input_data)
        
        # If prediction was successful, return the predicted value
        if predicted_value is not None:
            predicted_value = predicted_value[0]  # Get the scalar value from the array
            return {"predicted_subscription_status": f"{predicted_value:.2f} subscribers"}
        else:
            return Response("Prediction failed. Please check the input values.", status_code=400)
    
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return Response(f"Prediction failed: {e}", status_code=500)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)