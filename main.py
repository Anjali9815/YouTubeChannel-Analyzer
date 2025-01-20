from YouTubeChannelAnalyzer.logging import logger
from YouTubeChannelAnalyzer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline

logger.info("Welcome to YouTubeChannelAnalyzer")

STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e




