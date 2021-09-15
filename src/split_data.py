# split raw data
# save split data in data/processed folder

import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from get_data import read_params


def split_and_save(config_path):
    config = read_params(config_path)
    train_data_path = config['split_data']['train_path']
    val_data_path = config['split_data']['val_path']
    raw_data_path = config["load_data"]["raw_data"]
    split_ratio = config['split_data']['val_size']
    random_state = config['base']['random_state']

    df = pd.read_csv(raw_data_path, sep=',')
    train, validation = train_test_split(df, random_state=random_state, test_size=split_ratio)

    train.to_csv(train_data_path, sep=',', encoding = 'utf-8')
    validation.to_csv(val_data_path, sep=',', encoding = 'utf-8')


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    split_and_save(config_path=parsed_args.config)