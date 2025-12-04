import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

project_name = "mlproject_demo"

list_of_files = [
    f"src/{project_name}/api/__init__.py",
    f"src/{project_name}/api/main.py",
    f"src/{project_name}/api/predict.py",
    f"src/{project_name}/api/pydantic_schema.py",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/data/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/config.yaml",
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
    '.env',
    'dvc.lock',
    'params.yaml',
    '.dockerignore'
]


for filename in list_of_files:
    filename = Path(filename)
    filedir = filename.parent
    
    if not os.path.exists(filedir):
        os.makedirs(filedir)
        logging.info(f"Created directory: {filedir}")
    
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        with open(filename,'w') as f:
            pass

        logging.info(f"Created file : {filename}")