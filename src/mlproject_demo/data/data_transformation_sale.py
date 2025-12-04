import sys
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from src.mlproject_demo.utils.logger import logger
from src.mlproject_demo.utils.exception import CustomException
from src.mlproject_demo.utils.common import load_config,save_object
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    sale_data_path: str
    sale_transformed_path: str


class DataTransformationSale:
    def __init__(self):
        cfg = load_config()
        self.config = DataTransformationConfig(
            sale_data_path = cfg['transformed_sale']['sale_path'],
            sale_transformed_path = cfg['transformed_sale']['sale_transformed_path']
        )
        os.makedirs(self.config.sale_transformed_path,exist_ok = True)
        logger.info(f"Data Transformation for Sale is Initialized saved data in {self.config.sale_transformed_path}")
    

    def load_data(self):
        try:
            df = pd.read_csv(self.config.sale_data_path)
            logger.info(f"Rent Data loaded from path {self.config.sale_data_path} with shape {df.shape}")
    
            return df
        except Exception as e:
            raise CustomException(f"Data loaded Failed with error {e}",sys)
    
    def splitting_target_feature(self,df:pd.DataFrame):
        try:
            X = df.drop(columns = ['price'],axis = 1)
            y = df['price']
            logger.info(f"Target column price is splitted ")
            return X,y
        except Exception as e:
            raise CustomException(f"Error during splitting target feature {e}",sys)
    
    def create_preprocessor(self,X):
        try:
            numeric_features = X.select_dtypes(include = [np.number]).columns.tolist()
            categorical_features = X.select_dtypes(include = ['object']).columns.tolist()
            numeric_features.remove('MyUnknownColumn')

            logger.info(f"Numeric features are {numeric_features}")
            logger.info(f"Categorical features are {categorical_features}")

            numeric_piepline = Pipeline(steps = [
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler' , StandardScaler())]
            )
            categorical_pipeline = Pipeline(steps = [
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder(handle_unknown='ignore',sparse_output = False)),
                ('scaler', StandardScaler())]
            )

            preprocessor = ColumnTransformer(
                transformers =[
                    ('num',numeric_piepline,numeric_features),
                    ('cat',categorical_pipeline,categorical_features),
                ]
            )

            logger.info("Rent Prerpocessor pipeline created successfully")
            return preprocessor
        except Exception as e:
            raise CustomException(f"Error occured during preprocessing {e}",sys)

    def run(self):
        try:
            logger.info("Data Transformation Started")
            df = self.load_data()
            X,y = self.splitting_target_feature(df)
            preprocessor = self.create_preprocessor(X)
            X_preprocessed = preprocessor.fit_transform(X)


            # train test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_preprocessed, y, test_size = 0.2, random_state = 42
            )

            np.save(os.path.join(self.config.sale_transformed_path,'X_train.npy'),X_train)
            np.save(os.path.join(self.config.sale_transformed_path,'X_test.npy'),X_test)
            np.save(os.path.join(self.config.sale_transformed_path,'y_train.npy'),y_train)
            np.save(os.path.join(self.config.sale_transformed_path,'y_test.npy'),X_test)

            save_object(preprocessor,os.path.join(self.config.sale_transformed_path,'preprocessor.pkl'))

            logger.info("Transformed Rent Data Successfully")
        except Exception as e:
            raise CustomException(f"Error occured during Rent Transformation {e}",sys)

if __name__ == "__main__":
    data_transformation = DataTransformationSale()
    data_transformation.run()