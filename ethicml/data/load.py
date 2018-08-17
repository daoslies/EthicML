"""
Loads Data from .csv files
"""

import os
from typing import List, Dict
import pandas as pd

from ethicml.common import ROOT_DIR
from ethicml.data.configurable_dataset import ConfigurableDataset
from ethicml.data.dataset import Dataset


def load_data(dataset: Dataset) -> dict:
    filename = dataset.get_filename()
    data_loc: str = "{}/data/csvs/{}".format(ROOT_DIR, filename)
    dataframe: pd.DataFrame = pd.read_csv(data_loc)
    assert isinstance(dataframe, pd.DataFrame)

    feature_split = dataset.get_feature_split()

    x_data = dataframe[feature_split['x']]
    s_data = dataframe[feature_split['s']]
    y_data = dataframe[feature_split['y']]

    return {"x": x_data,
            "s": s_data,
            "y": y_data}


def create_data_obj(filepath: str, s_columns: List[str], y_columns: List[str]) -> Dataset:
    conf: ConfigurableDataset = ConfigurableDataset()
    conf.set_filename(os.path.basename(filepath))

    dataframe: pd.DataFrame = pd.read_csv(filepath)

    columns: List[str] = dataframe.columns.values.tolist()
    for s_col in s_columns:
        columns.remove(s_col)
    for y_col in y_columns:
        columns.remove(y_col)

    feat_split: Dict[str, List[str]] = {
        'x': columns,
        's': s_columns,
        'y': y_columns
    }
    conf.set_feature_split(feat_split)

    return conf
