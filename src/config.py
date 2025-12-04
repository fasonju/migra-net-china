# Keep class relative location to 
import os
from pathlib import Path
import platform
from types import ModuleType

# 获取项目根目录（假设config.py在项目根目录）
PROJECT_ROOT = Path(__file__).parent

class BaseConfig:
    data_folder: os.PathLike = PROJECT_ROOT / "data"
    china_provinces_path = data_folder / "china_provinces"
    data_csv_path = data_folder / "data.csv"
    output_path: os.PathLike = PROJECT_ROOT / "output"
    SEED: int = 42
    geo_data_subset = ['hometown_lon', 'hometown_lat', 'first_lon', 'first_lat', 'current_lon', 'current_lat']
