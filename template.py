import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

project_name = "mlproject"

list_of_files = [
    f"src/{project_name}/api/__init__.py",
    f"src/{project_name}/api/main.py",
    f"src/{project_name}/api/predict.py",
    f"src/{project_name}/api/pydantic_schema.py",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/data/__init__.py",
    f"src/{project_name}/data/data_ingestion.py",
    f"src/{project_name}/data/data_transformation_sale.py",
    f"src/{project_name}/data/data_transformation_rent.py",
    f"src/{project_name}/models/model_trainer.py",
    f"src/{project_name}/models/model_monitering.py",
    f"src/{project_name}/utils/exception.py",
    f"src/{project_name}/utils/logger.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "Readme.md",
    'setup.py',
    'dvc.yaml',
    'params.yaml',
    '.dockerignore'
]
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir = filepath.parent
    if not os.path.exists(filedir):
        os.makedirs(filedir)
        logging.info(f"Created directory: {filedir}")
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Created file: {filepath}")