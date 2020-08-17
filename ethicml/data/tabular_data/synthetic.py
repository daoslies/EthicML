"""Class to describe features of the Synthetic dataset."""
from warnings import warn

from ..dataset import Dataset

__all__ = ["Synthetic", "synthetic"]


def Synthetic() -> Dataset:  # pylint: disable=invalid-name
    """Dataset with synthetic scenario 1 data."""
    warn("The Synthetic class is deprecated. Use the function instead.", DeprecationWarning)
    return synthetic()


def synthetic(scenario: int = 1) -> Dataset:
    r"""Dataset with synthetic data.

    Scenario 1 = X⊥S & Y⊥S.
    """
    return Dataset(
        name="Synthetic - Scenario 1",
        num_samples=1000,
        filename_or_path="synthetic_scenario_1.csv",
        features=["x1", "x2"],
        cont_features=["x1", "x2"],
        sens_attrs=["s"],
        class_labels=["y"],
        discrete_only=False,
    )
