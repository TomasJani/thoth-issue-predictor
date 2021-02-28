"""Grid search helper module with results display."""

from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeClassifier


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
            "ccp_alpha": [0.0, 0.2, 0.3, 0.5, 0.8],
        }
    ]

    scores = ["precision", "recall"]

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(
            DecisionTreeClassifier(), tuned_parameters, scoring="%s_macro" % score
        )
        clf.fit(x_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        means = clf.cv_results_["mean_test_score"]
        stds = clf.cv_results_["std_test_score"]
        for mean, std, params in zip(means, stds, clf.cv_results_["params"]):
            print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(x_test)
        print(classification_report(y_true, y_pred))
        print()

        return clf.best_params_
