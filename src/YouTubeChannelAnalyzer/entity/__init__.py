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