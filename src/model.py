# load train and test
# train model
# save the metrics

import os
import pandas as pd
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.linear_model import ElasticNet
import argparse
import joblib
import json
from get_data import read_params


def eval_metrics(actual,pred):
    rmse = np.sqrt(mean_squared_error(actual,pred))
    mae = mean_absolute_error(actual,pred)
    r2 = r2_score(actual,pred)

    return rmse,mae,r2


def train_and_evaluate(config_path):
    config = read_params(config_path)
    train_data_path = config['split_data']['train_path']
    val_data_path = config['split_data']['val_path']
    random_state = config['base']['random_state']
    model_dir = config['model_dir']

    alpha=config['estimators']['ElasticNet']['params']['alpha']
    l1_ratio=config['estimators']['ElasticNet']['params']['l1_ratio']

    target = config["base"]['target_col']

    train = pd.read_csv(train_data_path, sep=',', encoding='utf-8')
    val = pd.read_csv(val_data_path, sep=',', encoding='utf-8')

    train_X = train.drop(target,axis=1)
    val_X = val.drop(target, axis=1)

    train_y = train[target]
    val_y = val[target]

    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state= random_state)
    lr.fit(train_X,train_y)

    prediction = lr.predict(val_X)

    (rmse, mae, r2) = eval_metrics(val_y, prediction)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)