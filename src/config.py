# Keep class relative location to 
import os
from pathlib import Path

class BaseConfig:
    data_folder: os.PathLike = "data"
    china_provinces_path = data_folder / "china_provinces"
    data_csv_path = data_folder / "data.csv"
    output_path: os.PathLike = "output"
    SEED: int = 42
    
