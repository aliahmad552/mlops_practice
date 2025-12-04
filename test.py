from src.mlproject_demo.utils.exception import CustomException
from src.mlproject_demo.utils.logger import logger
import sys
try: 
    a = 1/0

except Exception as e:
    raise CustomException(e, sys)