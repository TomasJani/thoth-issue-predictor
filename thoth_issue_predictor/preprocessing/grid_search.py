"""Grid search helper module with results display."""

import warnings

from catboost import CatBoostClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")


def grid_search_scikit(x, y):
    """Grid search helper function for Scikit Decision tree classifier."""
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.4, random_state=0
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

    clf = GridSearchCV(DecisionTreeClassifier(), tuned_parameters, scoring="roc_auc")
    clf.fit(x_train, y_train)

    return clf.best_params_


def grid_search_catboost(pool):
    """Grid search helper function for Scikit Catboost classifier."""
    params = {
        "verbose": False,
        "eval_metric": "AUC",
        "loss_function": "Logloss",
        "leaf_estimation_iterations": 10,
    }
    grid = {
        "iterations": [1000, 2000],
        "depth": [4, 5, 6, 7],
        "l2_leaf_reg": [3, 5, 7],
    }
    model = CatBoostClassifier(**params)
    search_results = model.grid_search(grid, X=pool, verbose=False)
    return {**search_results["params"], **params}
