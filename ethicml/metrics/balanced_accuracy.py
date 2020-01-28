"""Accuracy that is balanced with respect to the class labels."""

from ethicml.common import implements
from ethicml.utility import Prediction, DataTuple
from .confusion_matrix import confusion_matrix
from .metric import Metric


class BalancedAccuracy(Metric):
    """Accuracy that is balanced with respect to the class labels."""

    @implements(Metric)
    def score(self, prediction: Prediction, actual: DataTuple) -> float:
        t_neg, f_pos, f_neg, t_pos = confusion_matrix(prediction, actual, self.positive_class)
        tpr = t_pos / (t_pos + f_neg)
        tnr = t_neg / (t_neg + f_pos)
        return 0.5 * (tpr + tnr)

    @property
    def name(self) -> str:
        """Name of the algorithm."""
        return "Balanced Accuracy"