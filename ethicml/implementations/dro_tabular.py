"""Implementation of Fairness without Demographics."""
import json
import sys
from pathlib import Path
from typing import List, Union

import pandas as pd
import torch
from joblib import dump, load
from torch import optim
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader

from ethicml.algorithms.inprocess.fairness_wo_demographics import DroArgs
from ethicml.implementations.beutel import set_seed
from ethicml.implementations.dro_modules.dro_classifier import DROClassifier
from ethicml.implementations.pytorch_common import CustomDataset, TestDataset
from ethicml.implementations.utils import load_data_from_flags
from ethicml.utility import DataTuple, SoftPrediction, TestTuple


def train_model(
    epoch: int, model: DROClassifier, train_loader: DataLoader, optimizer: Optimizer
) -> None:
    """Train a model."""
    model.train()
    train_loss = 0.0
    for batch_idx, (data_x, _, data_y) in enumerate(train_loader):
        data_x = data_x.to("cpu")
        data_y = data_y.to("cpu")
        optimizer.zero_grad()
        y_prob = model.forward(data_x)
        loss = model.loss(y_prob, data_y)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        if batch_idx % 100 == 0:
            print(
                f"train Epoch: {epoch} [{batch_idx * len(data_x)}/{len(train_loader.dataset)}"  # type: ignore[arg-type]
                f"\t({100. * batch_idx / len(train_loader):.0f}%)]"
                f"\tLoss: {loss.item() / len(data_x):.6f}"
            )

    print(f"====> Epoch: {epoch} Average loss: {train_loss / len(train_loader.dataset):.4f}")  # type: ignore[arg-type]


def fit(train: DataTuple, args: DroArgs) -> DROClassifier:
    """Train a network and return predictions."""
    # Set up the data
    set_seed(args["seed"])
    train_data = CustomDataset(train)
    train_loader = DataLoader(train_data, batch_size=args["batch_size"])

    # Build Network
    model = DROClassifier(
        in_size=train_data.xdim,
        out_size=train_data.ydim,
        network_size=args["network_size"],
        eta=args["eta"],
    ).to("cpu")
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    # Run Network
    for epoch in range(int(args["epochs"])):
        train_model(epoch, model, train_loader, optimizer)
    return model


def predict(model: DROClassifier, test: TestTuple, args: DroArgs) -> SoftPrediction:
    """Train a network and return predictions."""
    # Set up the data
    test_data = TestDataset(test)
    test_loader = DataLoader(test_data, batch_size=args["batch_size"])

    # Transform output
    post_test: List[List[float]] = []
    model.eval()
    with torch.no_grad():
        for _x, _ in test_loader:
            out = model.forward(_x)
            post_test += out.data.tolist()

    return SoftPrediction(soft=pd.Series([j for i in post_test for j in i]))


def train_and_predict(train: DataTuple, test: TestTuple, args: DroArgs) -> SoftPrediction:
    """Train a network and return predictions."""
    # Set up the data
    set_seed(args["seed"])
    train_data = CustomDataset(train)
    train_loader = DataLoader(train_data, batch_size=args["batch_size"])

    test_data = TestDataset(test)
    test_loader = DataLoader(test_data, batch_size=args["batch_size"])

    # Build Network
    model = DROClassifier(
        in_size=train_data.xdim,
        out_size=train_data.ydim,
        network_size=args["network_size"],
        eta=args["eta"],
    ).to("cpu")
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    # Run Network
    for epoch in range(int(args["epochs"])):
        train_model(epoch, model, train_loader, optimizer)

    # Transform output
    post_test: List[List[float]] = []
    model.eval()
    with torch.no_grad():
        for _x, _ in test_loader:
            out = model.forward(_x)
            post_test += out.data.tolist()

    return SoftPrediction(soft=pd.Series([j for i in post_test for j in i]))


def main() -> None:
    """This function runs the FWD model as a standalone program on tabular data."""
    args: DroArgs = json.loads(sys.argv[1])
    data: Union[DataTuple, TestTuple]
    if args["mode"] == "run":
        assert "train" in args
        assert "test" in args
        assert "predictions" in args
        train, test = load_data_from_flags(args)
        train_and_predict(train, test, args).to_npz(Path(args["predictions"]))
    elif args["mode"] == "fit":
        assert "train" in args
        assert "model" in args
        data = DataTuple.from_npz(Path(args["train"]))
        model = fit(data, args)
        dump(model, Path(args["model"]))
    elif args["mode"] == "predict":
        assert "model" in args
        assert "predictions" in args
        assert "test" in args
        data = TestTuple.from_npz(Path(args["test"]))
        model = load(Path(args["model"]))
        predict(model, data, args).to_npz(Path(args["predictions"]))


if __name__ == "__main__":
    main()
