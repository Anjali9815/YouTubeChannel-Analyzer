from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path


@dataclass(frozen=True)
class DataTransformationConfig():
    root_dir: Path
    data_dir: Path


@dataclass(frozen= True)
class DataAnalysisConfig():
    root_dir: Path
    data_dir : Path


@dataclass(frozen= True)
class ModelTrainerconfig:
    root_dir : Path
    data_dir : Path
    test_size: float
    random_state_size: int
    n_estimators: int
    random_state : int