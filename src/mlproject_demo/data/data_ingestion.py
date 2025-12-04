from src.mlproject_demo.utils.logger import logger
from src.mlproject_demo.utils.exception import CustomException
from src.mlproject_demo.utils.common import load_config,load_sql_tabel,save_object
from dataclasses import dataclass
import pandas as pd
import sys
import os

@dataclass
class DataIngestionConfig:
    sql_table : str
    raw_path: str
    sale_path:str
    rent_path: str

class DataIngestion:
    def __init__(self):
        cfg = load_config()

        self.config = DataIngestionConfig(
            sql_table=cfg['data']['my_sql_table'],
            raw_path=cfg['data']['raw_path'],
            rent_path = cfg['data']['rent_path'],
            sale_path=cfg['data']['sale_path']
        )

        logger.info(f"Data Ingestion Initialized : sql_tabel : {self.config.sql_table}, ,sale_path: {self.config.sale_path},rent_path: {self.config.rent_path}")


    def fetched_data(self):
        try:
            logger.info(f"Fetching data from table {self.config.sql_table}")
            df = load_sql_tabel(self.config.sql_table)
            logger.info(f"Fetched Data succesffuly")
            if df.empty:
                logger.info("DataFrame is empty")

            return df
        
        except Exception as e:
            raise CustomException(e, sys)
    
    def save_raw_data(self,df: pd.DataFrame):
        
        try:
            os.makedirs(os.path.dirname(self.config.raw_path), exist_ok = True)
            df.to_csv(self.config.raw_path,index = False)
            logger.info(f"Raw Data saved succesfuly at path {self.config.raw_path}")

            df['purpose'] = df['purpose'].str.strip().str.lower()
            df_sale = df[df['purpose'] == 'for sale']
            df_rent = df[df['purpose'] == 'for rent']

            os.makedirs(os.path.dirname(self.config.rent_path),exist_ok = True)
            df_rent.to_csv(self.config.rent_path,index = False)
            logger.info(f"Rent Data saved at {self.config.rent_path}")

            os.makedirs(os.path.dirname(self.config.sale_path),exist_ok = True)
            df_sale.to_csv(self.config.sale_path,index = False)
            logger.info(f"Rent Data saved at {self.config.sale_path}")
        except Exception as e:
            raise CustomException(f"Data Ingestion failed {e}",sys)
    def run(self):

        logger.info("Data Ingestion Started")
        df = self.fetched_data()
        self.save_raw_data(df)
        logger.info("Data Ingestion succesffuly completed")


if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.run()
