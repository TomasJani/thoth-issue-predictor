"""Grid search helper module with results display."""

import warnings

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")


def grid_search(x, y):
    """Grid search helper function with results display."""
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.5, random_state=0
    )

    # Set the parameters by cross-validation
    tuned_parameters = [
        {
            "criterion": ["gini", "entropy"],
            "splitter": ["best", "random"],
            "max_depth": [3, 5, 8],
            "min_samples_split": [2, 5, 8],
            "min_samples_leaf": [1, 2, 3, 5],
            "random_state": [10, 20, 50, 100],
            "ccp_alpha": [0.2, 0.3, 0.5, 0.8],
        }
    ]

    scores = ["precision", "recall"]

    for score in scores:
        clf = GridSearchCV(
            DecisionTreeClassifier(), tuned_parameters, scoring="%s_macro" % score
        )
        clf.fit(x_train, y_train)

        return clf.best_params_
