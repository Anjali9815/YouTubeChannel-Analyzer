from YouTubeChannelAnalyzer.logging import logger
from YouTubeChannelAnalyzer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from YouTubeChannelAnalyzer.pipeline.satage_02_data_transformation import DataTransformationTrainingPipeline
from YouTubeChannelAnalyzer.pipeline.stage_03_data_analysis import DataAnalysisTrainingPipeline
from YouTubeChannelAnalyzer.pipeline.stage_04_model_trainer import ModelTrainingPipeline

# Global flag to track the pipeline running status
is_pipeline_running = False
training_status = "Not started"

def train_model(run_data_ingestion: bool = False, user_input: str = None):
    global is_pipeline_running, training_status

    try:
        is_pipeline_running = True
        training_status = "Training started"
        
        # Conditionally run Data Ingestion Stage
        if run_data_ingestion:
            STAGE_NAME = "Data Ingestion stage"
            logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
            data_ingestion_stage = DataIngestionTrainingPipeline(user_input=user_input)
            data_ingestion_stage.main()
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        else:
            logger.info("Skipping Data Ingestion stage.")

        # Data Transformation Stage (Always run)
        STAGE_NAME = "Data Transformation stage"
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_transformation_stage = DataTransformationTrainingPipeline()
        data_transformation_stage.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

        # Data Analysis Stage (Always run)
        STAGE_NAME = "Data Analysis stage"
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_analysis_stage = DataAnalysisTrainingPipeline()
        data_analysis_stage.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

        # Model Training Stage (Always run)
        STAGE_NAME = "Model Training stage"
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        model_training_stage = ModelTrainingPipeline()
        model_training_stage.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

        # After all stages are done, reset the flag and return success status
        is_pipeline_running = False
        training_status = "Done training"
        return {"status": "Done training"}

    except Exception as e:
        logger.exception(f"Error in training pipeline: {e}")
        is_pipeline_running = False  # Reset the flag in case of error
        training_status = "Error occurred"
        return {"status": "error", "message": str(e)}


# Data Transformation Stage (Always run)
STAGE_NAME = "Data Transformation stage"
logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
data_transformation_stage = DataTransformationTrainingPipeline()
data_transformation_stage.main()
logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

# Data Analysis Stage (Always run)
STAGE_NAME = "Data Analysis stage"
logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
data_analysis_stage = DataAnalysisTrainingPipeline()
data_analysis_stage.main()
logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

# Model Training Stage (Always run)
STAGE_NAME = "Model Training stage"
logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
model_training_stage = ModelTrainingPipeline()
model_training_stage.main()
logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
