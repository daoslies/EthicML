"""Accuracy and related metrics."""
from dataclasses import dataclass
from typing import Callable, Tuple
from typing_extensions import Protocol

import pandas as pd
from ranzen import implements
from sklearn.metrics import accuracy_score, f1_score

from ethicml.utility import DataTuple, Prediction

from .metric import Metric

__all__ = ["Accuracy", "F1", "SklearnMetric"]


class SklearnMetric(Metric, Protocol):
    """Wrapper around an sklearn metric."""

    # we have to store the callable in a 1-element tuple because otherwise mypy gets confused
    sklearn_metric: Tuple[Callable[[pd.DataFrame, pd.Series], float]]

    @implements(Metric)
    def score(self, prediction: Prediction, actual: DataTuple) -> float:
        return self.sklearn_metric[0](actual.y, prediction.hard)


@dataclass
class Accuracy(SklearnMetric):
    """Classification accuracy."""

    sklearn_metric = (accuracy_score,)
    apply_per_sensitive = True

    @property
    def name(self) -> str:
        """Name of the metric."""
        return "Accuracy"


@dataclass
class F1(SklearnMetric):
    """F1 score: harmonic mean of precision and recall."""

    sklearn_metric = (f1_score,)
    apply_per_sensitive = True

    @property
    def name(self) -> str:
        """Name of the metric."""
        return "F1"
