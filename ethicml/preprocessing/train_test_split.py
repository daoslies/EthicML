"""
Split into train and test data
"""
import itertools
from typing import Tuple, List, Iterator

import numpy as np
from numpy.random import RandomState
import pandas as pd
from pandas.testing import assert_index_equal

from ethicml.utility.data_structures import DataTuple
from ethicml.utility.data_helpers import shuffle_df


def train_test_split(
    data: DataTuple, train_percentage: float = 0.8, random_seed: int = 0, proportional: bool = False
) -> (Tuple[DataTuple, DataTuple]):
    """Split a data tuple into two datatuple along the rows of the DataFrames

    Args:
        data: data tuple to split
        train_percentage: percentage for train split
        random_seed: seed to make splitting reproducible
        proportional: if True, ensure that the proportion of s and y are the same in train and test

    Returns:
        train split and test split
    """
    if proportional:
        return _proportional_train_test_split(data, train_percentage, random_seed)

    # ======================== concatenate the datatuple to one dataframe =========================
    # save the column names for later
    x_columns: pd.Index = data.x.columns
    s_columns: pd.Index = data.s.columns
    y_columns: pd.Index = data.y.columns

    all_data: pd.DataFrame = pd.concat([data.x, data.s, data.y], axis="columns")

    all_data = shuffle_df(all_data, random_state=1)

    # ============================== split the concatenated dataframe =============================
    # permute
    all_data = shuffle_df(all_data, random_state=random_seed)

    # split
    train_len = int(train_percentage * len(all_data))
    all_data_train = all_data.iloc[:train_len]
    all_data_test = all_data.iloc[train_len:]

    assert isinstance(all_data_train, pd.DataFrame)
    assert isinstance(all_data_test, pd.DataFrame)

    all_data_train = all_data_train.reset_index(drop=True)
    all_data_test = all_data_test.reset_index(drop=True)

    # ================================== assemble train and test ==================================
    train: DataTuple = DataTuple(
        x=all_data_train[x_columns],
        s=all_data_train[s_columns],
        y=all_data_train[y_columns],
        name=f"{data.name} - Train",
    )

    test: DataTuple = DataTuple(
        x=all_data_test[x_columns],
        s=all_data_test[s_columns],
        y=all_data_test[y_columns],
        name=f"{data.name} - Test",
    )

    assert isinstance(train.x, pd.DataFrame)
    assert isinstance(test.x, pd.DataFrame)
    assert_index_equal(train.x.columns, x_columns)
    assert_index_equal(test.x.columns, x_columns)

    assert isinstance(train.s, pd.DataFrame)
    assert isinstance(test.s, pd.DataFrame)
    assert_index_equal(train.s.columns, s_columns)
    assert_index_equal(test.s.columns, s_columns)

    assert isinstance(train.y, pd.DataFrame)
    assert isinstance(test.y, pd.DataFrame)
    assert_index_equal(train.y.columns, y_columns)
    assert_index_equal(test.y.columns, y_columns)

    return train, test


def _proportional_train_test_split(
    data: DataTuple, train_percentage: float = 0.8, random_seed: int = 0
) -> (Tuple[DataTuple, DataTuple]):
    """Split a data tuple into two datatuple along the rows of the DataFrames"""
    random = RandomState(seed=random_seed)  # local random state that won't affect the global state
    s_col = data.s.columns[0]
    y_col = data.y.columns[0]

    s_vals: List[int] = list(map(int, data.s[s_col].unique()))
    y_vals: List[int] = list(map(int, data.y[y_col].unique()))

    train_empty: List[int] = []  # this is necessary because mypy is silly
    test_empty: List[int] = []
    train_idx: "np.ndarray[np.int32]" = np.array(train_empty, dtype=np.int32)
    test_idx: "np.ndarray[np.int32]" = np.array(test_empty, dtype=np.int32)

    # iterate over all combinations of s and y
    for s, y in itertools.product(s_vals, y_vals):
        # find all indices for this group
        idx: "np.ndarray[np.int32]"
        idx = ((data.s[s_col] == s) & (data.y[y_col] == y)).to_numpy().nonzero()[0]

        # shuffle and take subsets
        random.shuffle(idx)
        split_idx: int = round(len(idx) * train_percentage)
        # append index subsets to the list of train indices
        train_idx = np.concatenate([train_idx, idx[:split_idx]], axis=0)
        test_idx = np.concatenate([test_idx, idx[split_idx:]], axis=0)

    train: DataTuple = DataTuple(
        x=data.x.iloc[train_idx].reset_index(drop=True),
        s=data.s.iloc[train_idx].reset_index(drop=True),
        y=data.y.iloc[train_idx].reset_index(drop=True),
        name=f"{data.name} - Train",
    )

    test: DataTuple = DataTuple(
        x=data.x.iloc[test_idx].reset_index(drop=True),
        s=data.s.iloc[test_idx].reset_index(drop=True),
        y=data.y.iloc[test_idx].reset_index(drop=True),
        name=f"{data.name} - Test",
    )

    # assert that no data points got lost anywhere
    assert data.x.shape[0] == train.x.shape[0] + test.x.shape[0]
    assert data.s.shape[0] == train.s.shape[0] + test.s.shape[0]
    assert data.y.shape[0] == train.y.shape[0] + test.y.shape[0]

    # assert that we (at least approximately) achieved the specified `train_percentage`
    expected_train_len = round(data.x.shape[0] * train_percentage)
    # the maximum error occurs when all the group splits favor train or all favor test
    num_groups = len(s_vals) * len(y_vals)
    assert expected_train_len - num_groups < train.x.shape[0] < expected_train_len + num_groups

    return train, test


def fold_data(data: DataTuple, folds: int) -> Iterator[Tuple[DataTuple, DataTuple]]:
    """
    So much love to sklearn for making their source code open
    """

    indices: np.ndarray[np.int64] = np.arange(data.x.shape[0])

    fold_sizes: np.ndarray[np.int32] = np.full(folds, data.x.shape[0] // folds, dtype=np.int32)
    fold_sizes[: data.x.shape[0] % folds] += 1

    current = 0
    for i, fold_size in enumerate(fold_sizes):
        start, stop = current, current + fold_size
        val_inds: np.ndarray[np.int64] = indices[start:stop]
        train_inds = [i for i in indices if i not in val_inds]  # Pretty sure this is inefficient

        train_x = data.x.iloc[train_inds].reset_index(drop=True)
        train_s = data.s.iloc[train_inds].reset_index(drop=True)
        train_y = data.y.iloc[train_inds].reset_index(drop=True)

        assert train_x.shape == (len(train_inds), data.x.shape[1])
        assert train_s.shape == (len(train_inds), data.s.shape[1])
        assert train_y.shape == (len(train_inds), data.y.shape[1])

        val_x = data.x.iloc[val_inds].reset_index(drop=True)
        val_s = data.s.iloc[val_inds].reset_index(drop=True)
        val_y = data.y.iloc[val_inds].reset_index(drop=True)

        assert val_x.shape == (len(val_inds), data.x.shape[1])
        assert val_s.shape == (len(val_inds), data.s.shape[1])
        assert val_y.shape == (len(val_inds), data.y.shape[1])

        yield DataTuple(
            x=train_x, s=train_s, y=train_y, name=f"{data.name} - train fold {i}"
        ), DataTuple(x=val_x, s=val_s, y=val_y, name=f"{data.name} - test fold {i}")

        current = stop
