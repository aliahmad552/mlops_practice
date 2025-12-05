import os
import sys
import numpy as np
from dotenv import load_dotenv
import mlflow
import mlflow.xgboost
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score

from src.mlproject_demo.utils.logger import logger
from src.mlproject_demo.utils.exception import CustomException
from src.mlproject_demo.utils.common import save_object, load_config, load_params
from dataclasses import dataclass

load_dotenv()

@dataclass
class ModelTrainerSaleConfig:
    transformed_path: str
    model_path: str
    preprocessor_path:str
    mlflow_experiment: str
    param: dict


class TrainSaleModel:

    def __init__(self):
        cfg = load_config()
        cfg = cfg['training']
        params = load_params()
        self.config = ModelTrainerSaleConfig(
            transformed_path=cfg['sale']['transformed_path'],
            model_path = cfg['sale']['model_path'],
            preprocessor_path = cfg['sale']['preprocessor_path'],
            mlflow_experiment=cfg['sale']['mlflow_experiment'],
            param = params['model']['sale']
        )

        os.makedirs(os.path.dirname(self.config.model_path),exist_ok = True)
        logger.info(f"Model Sale Trainer Started and model saved at {self.config.model_path}")



    def load_data(self):
            try: 
                X_train = np.load(f"{self.config.transformed_path}/X_train.npy")
                X_test = np.load(f"{self.config.transformed_path}/X_test.npy")
                y_train = np.load(f"{self.config.transformed_path}/y_train.npy")
                y_test = np.load(f"{self.config.transformed_path}/y_test.npy")

                logger.info("Transformed Data loaded successfully for Sale Model Training")
                return X_train, X_test, y_train, y_test
        
            except Exception as e:
                raise CustomException(f"Error Occured During Data loadin in train sale file {e}",sys)
            
    def evaluate(self, model, X_test, y_test):
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(preds, y_test)
        return rmse, r2

    def run(self):
         
        mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))
        mlflow.set_experiment(self.config.mlflow_experiment)

        X_train, X_test, y_train, y_test = self.load_data()

        with mlflow.start_run():

            # ---------------- XGBoost Model ---------------- #
            model = XGBRegressor(
                n_estimators=self.config.param["n_estimators"],
                learning_rate=self.config.param["learning_rate"],
                max_depth=self.config.param["max_depth"],
                subsample=self.config.param["subsample"],
                colsample_bytree=self.config.param["colsample_bytree"],
                random_state=self.config.param["random_state"]
            )


            logger.info("Model Training Start for sale Data")
            model.fit(X_train, y_train)
            rmse, r2 = self.evaluate(model=model, X_test=X_test,y_test = y_test)

            mlflow.log_metric('rmse',rmse)
            mlflow.log_metric('r2',r2)

            for param_name, value in model.get_params().items():
                mlflow.log_param(param_name,value)

            mlflow.log_artifacts(self.config.transformed_path)

            save_object(model,self.config.model_path)
            logger.info("Best Sale model saved succesffuly in locally")

            mlflow.xgboost.log_model(xgb_model=model,artifact_path="sale_model")

            mlflow.register_model(model_uri = f"runs:/{mlflow.active_run().info.run_id}/{self.config.model_path}",
                                  name = "Sale Model")
            
            logger.info("Best Sale Model Logged Successfuly and regestered in registry")
        

if __name__ == "__main__":
    sale_training = TrainSaleModel()
    sale_training.run()

            
        

        

        
         