"""Abstract Base Class for all datasets that come with the framework."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional

from ethicml.common import ROOT_PATH
from ethicml.data.util import filter_features_by_prefixes, get_discrete_features

__all__ = ["Dataset"]


class Dataset(ABC):
    """Base class for datasets."""

    _features: List[str]
    _class_label_prefix: List[str]
    _class_labels: List[str]
    _s_prefix: List[str]
    _sens_attrs: List[str]
    _cont_features: List[str]
    _disc_features: List[str]
    _disc_feature_groups: Optional[Dict[str, List[str]]]

    def __init__(self, disc_feature_groups: Optional[Dict[str, List[str]]] = None) -> None:
        """Init Dataset object."""
        self._features: List[str] = []
        self._class_label_prefix: List[str] = []
        self._class_labels: List[str] = []
        self._s_prefix: List[str] = []
        self._sens_attrs: List[str] = []
        self._cont_features: List[str] = []
        self._disc_features: List[str] = []
        self.features_to_remove: List[str] = []
        self.discrete_only: bool = False
        self._filepath: Path = ROOT_PATH / "data" / "csvs" / self.filename
        self._disc_feature_groups = disc_feature_groups

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the dataset."""

    @property
    @abstractmethod
    def filename(self) -> str:
        """File from which to load the data."""

    @property
    def filepath(self) -> Path:
        """Filepath from which to load the data."""
        return self._filepath

    @filepath.setter
    def filepath(self, loc: Path) -> None:
        """Setter for the filepath."""
        self._filepath = loc

    @property
    def ordered_features(self) -> Dict[str, List[str]]:
        """Return an order features dictionary.

        This should have separate entries for the features, the labels and the
        sensitive attributes, but the x features are ordered so first are the discrete features,
        then the continuous.
        """
        return {
            "x": self.discrete_features + self.continuous_features,
            "s": self._sens_attrs,
            "y": self._class_labels,
        }

    @property
    def feature_split(self) -> Dict[str, List[str]]:
        """Return a feature split dictionary.

        This should have separate entries for the features, the labels and the sensitive attributes.
        """
        if self.discrete_only:
            self.features_to_remove += self.continuous_features

        return {
            "x": filter_features_by_prefixes(self.features, self.features_to_remove),
            "s": self._sens_attrs,
            "y": self._class_labels,
        }

    @property
    def continuous_features(self) -> List[str]:
        """List of features that are continuous."""
        return filter_features_by_prefixes(self._cont_features, self.features_to_remove)

    @continuous_features.setter
    def continuous_features(self, feats: List[str]) -> None:
        self._cont_features = feats

    @property
    def features(self) -> List[str]:
        """List of all features."""
        return self._features

    @features.setter
    def features(self, feats: List[str]) -> None:
        self._features = feats

    @property
    def s_prefix(self) -> List[str]:
        """List of prefixes of the sensitive attribute."""
        return self._s_prefix

    @s_prefix.setter
    def s_prefix(self, sens_attrs: List[str]) -> None:
        self._s_prefix = sens_attrs
        self.features_to_remove += sens_attrs

    @property
    def sens_attrs(self) -> List[str]:
        """List of sensitive attributes."""
        return self._sens_attrs

    @sens_attrs.setter
    def sens_attrs(self, sens_attrs: List[str]) -> None:
        self._sens_attrs = sens_attrs

    @property
    def class_labels(self) -> List[str]:
        """List of class labels."""
        return self._class_labels

    @class_labels.setter
    def class_labels(self, labels: List[str]) -> None:
        self._class_labels = labels

    @property
    def class_label_prefix(self) -> List[str]:
        """List of prefixes of class labels."""
        return self._class_label_prefix

    @class_label_prefix.setter
    def class_label_prefix(self, label_prefixs: List[str]) -> None:
        self._class_label_prefix = label_prefixs
        self.features_to_remove += label_prefixs

    @property
    def discrete_features(self) -> List[str]:
        """List of features that are discrete."""
        return get_discrete_features(
            self.features, self.features_to_remove, self.continuous_features
        )

    @discrete_features.setter
    def discrete_features(self, feats: List[str]) -> None:
        self._disc_features = feats

    @property
    def disc_feature_groups(self) -> Optional[Dict[str, List[str]]]:
        """Dictionary of feature groups."""
        if self._disc_feature_groups is None:
            return None
        return {
            k: v for k, v in self._disc_feature_groups.items() if k not in self.features_to_remove
        }

    @abstractmethod
    def __len__(self) -> int:
        """Number of elements in the dataset."""
