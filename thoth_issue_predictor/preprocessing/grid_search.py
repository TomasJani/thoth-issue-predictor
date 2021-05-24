"""Grid search helper module with results display."""
import warnings

from catboost import CatBoostClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")


def grid_search_scikit(x, y):
    """Grid search helper function for Scikit Decision tree classifier."""
    tuned_parameters = [
        {
            "splitter": ["best", "random"],
            "max_depth": [3, 4, 5, 6],
            "min_samples_split": [3, 5, 7, 9, 10, 15],
            "min_samples_leaf": [3, 5, 7, 9, 10, 15],
        }
    ]

    clf = GridSearchCV(DecisionTreeClassifier(), tuned_parameters, scoring="roc_auc")
    clf.fit(x, y)

    return clf.best_params_


def grid_search_catboost(pool):
    """Grid search helper function for Scikit Catboost classifier."""
    params = {
        "verbose": False,
        "eval_metric": "AUC",
        "loss_function": "Logloss",
    }
    grid = {
        "grow_policy": ["SymmetricTree", "Depthwise", "Lossguide"],
        "iterations": [1000, 2000],
        "depth": [3, 4, 5, 6],
        "min_data_in_leaf": [3, 5, 7, 10],
    }
    model = CatBoostClassifier(**params)
    search_results = model.grid_search(grid, X=pool, verbose=False)
    return {**search_results["params"], **params}
