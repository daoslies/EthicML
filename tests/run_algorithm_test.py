"""
Test that an algorithm can run against some data
"""

from typing import Tuple, Dict
import pandas as pd
import numpy as np

from algorithms.inprocess.in_algorithm import InAlgorithm
from algorithms.inprocess.logistic_regression import LR
from algorithms.inprocess.svm import SVM
from algorithms.preprocess.beutel import Beutel
from data.test import Test
from data.load import load_data
from evaluators.evaluate_models import evaluate_models
from metrics.accuracy import Accuracy
from metrics.tpr import TPR
from preprocessing.train_test_split import train_test_split


def get_train_test():
    data: Dict[str, pd.DataFrame] = load_data(Test())
    train_test: Tuple[Dict[str, pd.DataFrame], Dict[str, pd.DataFrame]] = train_test_split(data)
    return train_test


def test_can_load_test_data():
    train, test = get_train_test()
    assert train is not None
    assert test is not None


def test_can_make_predictions():
    train, test = get_train_test()

    model: InAlgorithm = SVM()
    assert model is not None
    assert model.name == "SVM"

    predictions: pd.DataFrame = model.run(train, test)
    assert predictions[predictions.values == 1].count().values[0] == 201
    assert predictions[predictions.values == -1].count().values[0] == 199


def test_lr():
    train, test = get_train_test()

    model: InAlgorithm = LR()
    assert model is not None
    assert model.name == "Logistic Regression"

    predictions: np.array = model.run(train, test)
    assert predictions[predictions.values == 1].count().values[0] == 211
    assert predictions[predictions.values == -1].count().values[0] == 189


def test_beutel():
    train, test = get_train_test()

    model: InAlgorithm = Beutel()
    assert model is not None
    assert model.name == "Beutel"

    new_xtrain_xtest: Tuple[pd.DataFrame, pd.DataFrame] = model.run(train, test)
    new_xtrain: pd.DataFrame = new_xtrain_xtest[0]
    new_xtest: pd.DataFrame = new_xtrain_xtest[1]

    assert new_xtrain.shape[0] == train['x'].shape[0]
    assert new_xtest.shape[0] == test['x'].shape[0]

    new_train = {
        'x': new_xtrain,
        's': train['s'],
        'y': train['y']
    }

    new_test = {
        'x': new_xtest,
        's': test['s'],
        'y': test['y']
    }

    model: InAlgorithm = SVM()
    assert model is not None
    assert model.name == "SVM"

    predictions: pd.DataFrame = model.run(new_train, new_test)
    assert predictions[predictions.values == 1].count().values[0] == 208
    assert predictions[predictions.values == -1].count().values[0] == 192


def test_run_alg_suite():
    datasets = [Test()]
    models = [SVM(), LR()]
    metrics = [Accuracy()]
    per_sens_metrics = [Accuracy(), TPR()]
    result = evaluate_models(datasets, models, metrics, per_sens_metrics)

    result.to_csv("../results/res.csv", index=False)