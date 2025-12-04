import logging
import os
from datetime import datetime

logger_dir = os.path.join(os.getcwd(),'logs')
os.makedirs(logger_dir, exist_ok=True)

logger_file = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logger_file_path = os.path.join(logger_dir,logger_file)

logging.basicConfig(
    filename=logger_file_path,
    level = logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)