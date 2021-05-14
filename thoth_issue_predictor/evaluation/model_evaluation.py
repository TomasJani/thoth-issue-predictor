"""Implementation of evaluation class for model metrics."""
from datetime import datetime

from matplotlib import pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    plot_confusion_matrix,
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
        self.accuracy_score: float = 0
        self.f1_weighted: float = 0
        self.f1_micro: float = 0
        self.f1_macro: float = 0
        self.number_of_errors: int = 0

    def predict_and_save(self):
        """Predict the model and save the metrics from prediction."""
        start = datetime.now()
        self.y_pred = self.clf.predict(self.x_test)
        end = datetime.now()
        self.prediction_time = end - start
        self.auc = roc_auc_score(self.y_test, self.y_pred)
        self.accuracy_score = accuracy_score(self.y_test, self.y_pred)
        self.f1_weighted = f1_score(self.y_test, self.y_pred, average="weighted")
        self.f1_micro = f1_score(self.y_test, self.y_pred, average="micro")
        self.f1_macro = f1_score(self.y_test, self.y_pred, average="macro")
        self.number_of_errors: int = (self.y_pred != self.y_test).sum()

    def print(self):
        """Print evaluation metrics fro given model."""
        print(f"Train time: {self.train_time}")
        print(f"Number of errors: {self.number_of_errors}")
        print(f"AUC: {roc_auc_score(self.y_test, self.y_pred)}")
        print(f"Accuracy Score: {accuracy_score(self.y_test, self.y_pred)}")
        print(f"F1 weighted: {f1_score(self.y_test, self.y_pred, average='weighted')}")
        print(f"F1 micro: {f1_score(self.y_test, self.y_pred, average='micro')}")
        print(f"F1 macro: {f1_score(self.y_test, self.y_pred, average='macro')}")

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
        plt.savefig(f"./trees/{self.model_name}_matrix.pdf")
        plt.show()
