"""Implementation of evaluation class for model metrics."""
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
)

from thoth_issue_predictor.evaluation.urils import plot_confusion_matrix


class ModelEvaluation:
    """Implementation of evaluation class for model metrics."""

    def __init__(self, model_name, train_time, y_true, y_pred):
        """Initialize object attributes."""
        self.y_true = y_true
        self.y_pred = y_pred
        self.train_time: int = train_time
        self.model_name: str = model_name
        self.auc = roc_auc_score(self.y_true, self.y_pred)
        self.accuracy_score = accuracy_score(self.y_true, self.y_pred)
        self.f1_weighted = f1_score(self.y_true, self.y_pred, average="weighted")
        self.f1_micro = f1_score(self.y_true, self.y_pred, average="micro")
        self.f1_macro = f1_score(self.y_true, self.y_pred, average="macro")
        self.number_of_errors: int = (y_pred != y_true).sum()

    def print(self):
        """Print evaluation metrics fro given model."""
        print(f"Train time: {self.train_time}")
        print(f"Number of errors: {self.number_of_errors}")
        print(f"AUC: {roc_auc_score(self.y_true, self.y_pred)}")
        print(f"Accuracy Score: {accuracy_score(self.y_true, self.y_pred)}")
        print(f"F1 weighted: {f1_score(self.y_true, self.y_pred, average='weighted')}")
        print(f"F1 micro: {f1_score(self.y_true, self.y_pred, average='micro')}")
        print(f"F1 macro: {f1_score(self.y_true, self.y_pred, average='macro')}")

        print(classification_report(self.y_true, self.y_pred))
        cm = confusion_matrix(self.y_true, self.y_pred)
        print(cm)
        plot_confusion_matrix(
            cm,
            ["True", "False"],
            title=f"Confusion matrix for {self.model_name} model",
            normalize=False,
        )
