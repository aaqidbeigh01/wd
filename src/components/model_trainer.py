import os
import sys
from dataclasses import dataclass
from sklearn.ensemble import AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from src.exception import CustomException
from src.logger import logging
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from src.utils import save_obj,evaluate_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info('Splitting training and test data')
            x_tr,y_tr,x_te,y_te=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                'Random F' :RandomForestRegressor(),
                'Decision' :DecisionTreeRegressor(),
                'Gradient': GradientBoostingRegressor(),
                'Linear r': LinearRegression(),
                'XGB':XGBRegressor(),
                "Cat":CatBoostRegressor(verbose=False),
                'KNN':KNeighborsRegressor(),
                'Ada':AdaBoostRegressor(),
            }
            model_report:dict=evaluate_model(x_train=x_tr,y_train=y_tr,x_test=x_te,y_test=y_te,models=models)
            
            best_model_score=max(sorted(model_report.values()))
            
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]

            if best_model_score<0.6:
                raise CustomException('NO BEST MODEL FOUND')
            
            logging.info('bEST moDEL FOUNd')

            save_obj(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            predicted=best_model.predict(x_te)
            r2=r2_score(y_te,predicted)
            return r2

        except Exception as e:
            raise CustomException(e,sys)
            
