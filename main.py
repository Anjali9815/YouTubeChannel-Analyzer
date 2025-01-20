from YouTubeChannelAnalyzer.logging import logger
from YouTubeChannelAnalyzer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from YouTubeChannelAnalyzer.pipeline.satage_02_data_transformation import DataTransformationTrainingPipeline
from YouTubeChannelAnalyzer.pipeline.stage_03_data_analysis import DataAnalysisTrainingPipeline
from YouTubeChannelAnalyzer.pipeline.stage_04_model_trainer import ModelTrainingPipeline


logger.info("Welcome to YouTubeChannelAnalyzer")

STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion_stage = DataIngestionTrainingPipeline()
   data_ingestion_stage.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e


STAGE_NAME = "Data Transformation stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_transformation_sage = DataTransformationTrainingPipeline()
   data_transformation_sage.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e


STAGE_NAME = "Data Analysis stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_analysis_stage = DataAnalysisTrainingPipeline()
   data_analysis_stage.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e


STAGE_NAME = "Model Training stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   model_training_stage = ModelTrainingPipeline()
   model_training_stage.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e






