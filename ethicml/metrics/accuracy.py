"""Accuracy and related metrics."""
from dataclasses import dataclass
from typing import Callable, ClassVar, Tuple
from typing_extensions import Protocol

import pandas as pd
from ranzen import implements
from sklearn.metrics import accuracy_score, f1_score

from ethicml.utility import DataTuple, Prediction

from .metric import BaseMetric

__all__ = ["Accuracy", "F1", "SklearnMetric", "RobustAccuracy"]


class SklearnMetric(BaseMetric, Protocol):
    """Wrapper around an sklearn metric."""

    # we have to store the callable in a 1-element tuple because otherwise mypy gets confused
    sklearn_metric: ClassVar[Tuple[Callable[[pd.DataFrame, pd.Series], float]]]

    @implements(BaseMetric)
    def score(self, prediction: Prediction, actual: DataTuple) -> float:
        return self.sklearn_metric[0](actual.y, prediction.hard)


@dataclass
class Accuracy(SklearnMetric):
    """Classification accuracy."""

    sklearn_metric = (accuracy_score,)
    apply_per_sensitive: ClassVar[bool] = True
    _name: ClassVar[str] = "Accuracy"


@dataclass
class F1(SklearnMetric):
    """F1 score: harmonic mean of precision and recall."""

    sklearn_metric = (f1_score,)
    apply_per_sensitive: ClassVar[bool] = True
    _name: ClassVar[str] = "F1"


@dataclass
class RobustAccuracy(SklearnMetric):
    """Minimum Classification accuracy across S-groups."""

    sklearn_metric = (accuracy_score,)
    apply_per_sensitive: ClassVar[bool] = False
    _name: ClassVar[str] = "Robust Accuracy"

    @implements(SklearnMetric)
    def score(self, prediction: Prediction, actual: DataTuple) -> float:
        score_func = super().score
        return min(
            [
                score_func(prediction.get_s_subset(actual.s, _s), actual.get_s_subset(_s))
                for _s in actual.s[actual.s.columns[0]].unique()
            ]
        )
