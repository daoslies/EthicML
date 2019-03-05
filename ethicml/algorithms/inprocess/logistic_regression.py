"""
Wrapper around Sci-Kit Learn Logistic Regression
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression

from ethicml.algorithms.inprocess.in_algorithm import InAlgorithm
from ethicml.algorithms.utils import DataTuple


class LR(InAlgorithm):

    """Logistic regression with hard predictions"""
    def run(self, train: DataTuple, test: DataTuple, sub_process=False) -> pd.DataFrame:
        if sub_process:
            return self.run_threaded(train, test)

        clf = LogisticRegression(solver='liblinear', random_state=888)
        clf.fit(train.x, train.y.values.ravel())
        return pd.DataFrame(clf.predict(test.x), columns=["preds"])


    @property
    def name(self) -> str:
        return "Logistic Regression"


def main():
    """main method to run model"""
    model = LR()
    train, test = model.load_data()
    model.save_predictions(model.run(train, test))


if __name__ == "__main__":
    main()
