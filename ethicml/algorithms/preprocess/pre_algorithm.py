"""
Abstract Base Class of all algorithms in the framework
"""

from abc import abstractmethod
from typing import Tuple
import pandas as pd

from ..algorithm_base import Algorithm
from ..utils import get_subset, DataTuple


class PreAlgorithm(Algorithm):
    """Abstract Base Class for all algorithms that do pre-processing"""
    @abstractmethod
    def run(self, train: DataTuple, test: DataTuple) -> (
            Tuple[pd.DataFrame, pd.DataFrame]):
        """Generate fair features

        Args:
            train:
            test:
        """
        raise NotImplementedError("Run needs to be implemented")

    def run_test(self, train: DataTuple, test: DataTuple) -> (
            Tuple[pd.DataFrame, pd.DataFrame]):
        """

        Args:
            train:
            test:

        Returns:

        """
        train_testing = get_subset(train)
        return self.run(train_testing, test)