from src.mlproject_demo.utils.logger import logger
from src.mlproject_demo.utils.exception import CustomException
from dotenv import load_dotenv
import yaml
import pymysql
import pandas as pd
import os
import pickle
import sys

load_dotenv()


def load_config(path = 'src/mlproject_demo/config/config.yaml'):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    return config

host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv('db')

def validate_mysql_credentials():
    """Validates that all MySQL environment variables exist."""
    missing = []

    if not host:
        missing.append("host")
    if not user:
        missing.append("user")
    if password is None:
        missing.append("password")
    if not db:
        missing.append("db")

    if missing:
        raise CustomException(
            f"Missing MySQL credentials in .env file: {', '.join(missing)}",
            sys
        )
    
def load_sql_tabel(tabel_name):

    logger.info("Fetching data from my sql table")
    validate_mysql_credentials()

    try:
        connection = pymysql.connect(
            host = host,
            user = user,
            password= password,
            database = db
        )

        logger.info(f"Connection from MySQL Successful {host} - {db}")

        query = f"Select * from {tabel_name}"

        df = pd.read_sql_query(query,connection)
        logger.info(f"Data Fetech {df.shape[0]} rows and {df.shape[1]} columns")

        return df
    except Exception as e:
        raise CustomException(e, sys)
    

def save_object(obj,path):
    
    try:
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(obj , f)
        logger.info(f"Object saved at  {path}")
        
    except Exception as e:
        raise CustomException(f"Failed saving the object {e}", sys)
