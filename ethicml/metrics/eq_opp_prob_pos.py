"""
Used for claculating the probability of being poisitive given the class label is one... performs the same as TPR per
class, but does it in a different way.
"""


from typing import Dict

import numpy
import pandas

from ethicml.algorithms.utils import make_dict
from ethicml.metrics.confusion_matrix import confusion_matrix
from ethicml.metrics.metric import Metric


def pos_subset_test(preds: numpy.array, data: Dict[str, pandas.DataFrame]):
    y_ = data['y']

    return preds[y_ == 1]


def pos_subset_data(data: Dict[str, pandas.DataFrame]):
    features = data['x']
    sensitive_labels = data['s']
    class_labels = data['y']

    pos_x = features[class_labels == 1]
    pos_s = sensitive_labels[class_labels == 1]
    pos_y = class_labels[class_labels == 1]

    return make_dict(pos_x, pos_s, pos_y)


class EqOppProbPos(Metric):

    def score(self, prediction: numpy.array, actual: Dict[str, pandas.DataFrame]) -> float:
        pos_subset = pos_subset_data(actual)
        test_pos_subset = pos_subset_test(prediction, actual)

        _, f_pos, _, t_pos = confusion_matrix(test_pos_subset, pos_subset)

        return (t_pos + f_pos) / test_pos_subset.size

    @property
    def name(self) -> str:
        pass
