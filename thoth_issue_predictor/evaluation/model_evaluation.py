"""Implementation of evaluation class for model metrics."""
from datetime import datetime

from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    plot_confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)


class ModelEvaluation:
    """Implementation of evaluation class for model metrics."""

    def __init__(self, model_name, clf, train_time, x_test, y_test):
        """Initialize object attributes."""
        self.x_test = x_test
        self.y_test = y_test
        self.y_pred = None
        self.clf = clf
        self.train_time: int = train_time
        self.model_name: str = model_name
        self.prediction_time: float = 0
        self.auc: float = 0
        self.accuracy: float = 0
        self.precision: float = 0
        self.recall: float = 0
        self.f1: float = 0
        self.number_of_errors: int = 0

    def predict_and_save(self):
        """Predict the model and save the metrics from prediction."""
        start = datetime.now()
        self.y_pred = self.clf.predict(self.x_test)
        end = datetime.now()
        self.prediction_time = end - start
        self.auc = roc_auc_score(self.y_test, self.y_pred)
        self.accuracy = accuracy_score(self.y_test, self.y_pred)
        self.precision = precision_score(self.y_test, self.y_pred)
        self.recall = recall_score(self.y_test, self.y_pred)
        self.f1 = f1_score(self.y_test, self.y_pred)
        self.number_of_errors: int = (self.y_pred != self.y_test).sum()

    def print(self):
        """Print evaluation metrics fro given model."""
        print(f"Train time: {self.train_time}")
        print(f"Prediction time: {self.prediction_time}")
        print(f"Number of errors: {self.number_of_errors}")
        print(f"AUC: {self.auc}")
        print(f"Accuracy: {self.accuracy}")
        print(f"Precision: {self.precision}")
        print(f"Recall: {self.recall}")
        print(f"F1: {self.f1}")

        print(classification_report(self.y_test, self.y_pred))

        cm = plot_confusion_matrix(
            self.clf,
            self.x_test,
            self.y_test,
            display_labels=["Valid", "Failed"],
            cmap=plt.cm.Blues,
        )
        cm.ax_.set_title(f"Confusion matrix for {self.model_name}")

        print(f"Confusion matrix for {self.model_name}")
        print(cm.confusion_matrix)
        plt.grid(False)
        plt.savefig(f"./visualizations/{self.model_name}_matrix.pdf")
        plt.show()

        metrics.plot_roc_curve(self.clf, self.x_test, self.y_test)
        plt.savefig(f"./visualizations/{self.model_name}_roc.pdf")
        plt.show()
