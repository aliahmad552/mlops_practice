from src.mlproject_demo.utils.logger import logger
from src.mlproject_demo.utils.exception import CustomException
from src.mlproject_demo.utils.common import load_config
from dataclasses import dataclass



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

    

if __name__ == '__main__':
    data_ingestion = DataIngestion()

