from fastapi import FastAPI, BackgroundTasks, Query, Response
from main import train_model  # Importing the function from trainer.py
import logging

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
