"""
implementation of the upsampling method
"""
import itertools
from typing import Optional, List, Dict, Tuple

import pandas as pd

from ethicml.algorithms.inprocess import LRProb
from ethicml.implementations.utils import (
    PreAlgoArgs,
    load_data_from_flags,
    save_transformations,
)
from ethicml.utility import DataTuple, TestTuple


def concat_datatuples(first_dt: DataTuple, second_dt: DataTuple) -> DataTuple:
    """Given 2 datatuples, concatenate them and shuffle"""
    assert (first_dt.x.columns == second_dt.x.columns).all()
    assert (first_dt.s.columns == second_dt.s.columns).all()
    assert (first_dt.y.columns == second_dt.y.columns).all()

    x_columns: pd.Index = first_dt.x.columns
    s_columns: pd.Index = first_dt.s.columns
    y_columns: pd.Index = first_dt.y.columns

    a_combined: pd.DataFrame = pd.concat([first_dt.x, first_dt.s, first_dt.y], axis="columns")
    b_combined: pd.DataFrame = pd.concat([second_dt.x, second_dt.s, second_dt.y], axis="columns")

    combined: pd.DataFrame = pd.concat([a_combined, b_combined], axis="index")
    combined = combined.sample(frac=1.0, random_state=1).reset_index(drop=True)

    return DataTuple(
        x=combined[x_columns], s=combined[s_columns], y=combined[y_columns], name=first_dt.name
    )


def upsample(dataset: DataTuple, flags: Dict[str, str]) -> DataTuple:
    """Upsample a datatuple"""
    s_col = dataset.s.columns[0]
    y_col = dataset.y.columns[0]

    s_vals: List[int] = list(map(int, dataset.s[s_col].unique()))
    y_vals: List[int] = list(map(int, dataset.y[y_col].unique()))

    groups = itertools.product(s_vals, y_vals)

    data: Dict[Tuple[int, int], DataTuple] = {}
    for s, y in groups:
        s_y_mask = (dataset.s[s_col] == s) & (dataset.y[y_col] == y)
        data[(s, y)] = DataTuple(
            x=dataset.x.loc[s_y_mask].reset_index(drop=True),
            s=dataset.s.loc[s_y_mask].reset_index(drop=True),
            y=dataset.y.loc[s_y_mask].reset_index(drop=True),
            name=dataset.name,
        )

    percentages: Dict[Tuple[int, int], float] = {}

    vals: List[int] = []
    for key, val in data.items():
        vals.append(val.x.shape[0])

    for key, val in data.items():
        if flags['strategy'] == "naive":
            percentages[key] = max(vals) / val.x.shape[0]
        else:
            s_val: int = key[0]
            y_val: int = key[1]

            y_eq_y = dataset.y.loc[dataset.y[y_col] == y_val].count().to_numpy()[0]
            s_eq_s = dataset.s.loc[dataset.s[s_col] == s_val].count().to_numpy()[0]

            num_samples = dataset.y.count().to_numpy()[0]
            num_batch = val.y.count().to_numpy()[0]

            percentages[key] = round((y_eq_y * s_eq_s / (num_batch * num_samples)), 8)

    x_columns: pd.Index = dataset.x.columns
    s_columns: pd.Index = dataset.s.columns
    y_columns: pd.Index = dataset.y.columns

    upsampled: Dict[Tuple[int, int], DataTuple] = {}
    for key, val in data.items():
        all_data: pd.DataFrame = pd.concat([val.x, val.s, val.y], axis="columns")
        all_data = all_data.sample(frac=percentages[key], random_state=1, replace=True).reset_index(
            drop=True
        )
        upsampled[key] = DataTuple(
            x=all_data[x_columns], s=all_data[s_columns], y=all_data[y_columns], name=dataset.name
        )

    upsampled_datatuple: Optional[DataTuple] = None
    for key, val in upsampled.items():
        if upsampled_datatuple is None:
            upsampled_datatuple = val
        else:
            upsampled_datatuple = concat_datatuples(upsampled_datatuple, val)

    if flags['strategy'] == "preferential":
        ranker = LRProb()
        rank = ranker.run(dataset, dataset)

        selected: List[pd.DataFrame] = []

        all_data = pd.concat([dataset.x, dataset.s, dataset.y], axis="columns")
        all_data = pd.concat([all_data, rank], axis="columns")

        for key, val in data.items():

            s_val = key[0]
            y_val = key[1]
            s_y_mask = (dataset.s[s_col] == s_val) & (dataset.y[y_col] == y_val)

            ascending = False
            if s_val <= 0:
                ascending = True

            if percentages[key] > 1.0:
                selected.append(all_data.loc[s_y_mask])
                percentages[key] -= 1.0

            weight = all_data.loc[s_y_mask][y_col].count()
            selected.append(
                all_data.loc[s_y_mask]
                .sort_values(by=['preds'], ascending=ascending)
                .iloc[: int(percentages[key] * weight)]
            )

        upsampled_dataframes: pd.DataFrame
        for i, df in enumerate(selected):
            if i == 0:
                upsampled_dataframes = df.drop(['preds'], axis="columns")
            else:
                upsampled_dataframes = pd.concat(
                    [upsampled_dataframes, df.drop(['preds'], axis="columns")], axis="index"
                ).reset_index(drop=True)
        upsampled_datatuple = DataTuple(
            x=upsampled_dataframes[x_columns],
            s=upsampled_dataframes[s_columns],
            y=upsampled_dataframes[y_columns],
            name=dataset.name,
        )

    assert upsampled_datatuple is not None
    return upsampled_datatuple


def train_and_transform(
    train: DataTuple, test: TestTuple, flags: Dict[str, str]
) -> Tuple[DataTuple, TestTuple]:
    """
    Train and transform function for the upsampler method
    """
    upsampled_train = upsample(train, flags)

    return upsampled_train, TestTuple(x=test.x, s=test.s, name=test.name)


class UpsamplerArgs(PreAlgoArgs):
    strategy: str


def main() -> None:
    """This function runs the Upsampler as a standalone program"""
    args = UpsamplerArgs()
    args.parse_args()

    flags = args.as_dict()

    train, test = load_data_from_flags(flags)
    save_transformations(train_and_transform(train, test, flags), args)


if __name__ == "__main__":
    main()
