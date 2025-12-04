from src.mlproject_demo.utils.logger import logger
from src.mlproject_demo.utils.exception import CustomException
import yaml

def load_config(path = 'src/mlproject_demo/config/config.yaml'):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    return config

