"""Implementation of metrics handler class for ModelEvaluation."""
import operator
from typing import Dict, List

import matplotlib.pyplot as plt
import seaborn as sn

from thoth_issue_predictor.evaluation.model_evaluation import ModelEvaluation


class Metrics:
    """Implementation of metrics handler class for ModelEvaluation."""

    descending_metrics: List[str] = ["accuracy", "auc", "f1", "precision", "recall"]

    def __init__(self, models: List[ModelEvaluation]):
        """Initialize object attributes."""
        self.model_metrics: Dict[str, List] = {
            "train_time": [],
            "prediction_time": [],
            "number_of_errors": [],
            "auc": [],
            "accuracy": [],
            "precision": [],
            "recall": [],
            "f1": [],
        }
        for model in models:
            self._add_metric(model, "train_time")
            self.model_metrics["prediction_time"].append(
                (model.model_name, model.prediction_time)
            )
            self.model_metrics["number_of_errors"].append(
                (model.model_name, model.number_of_errors)
            )
            self.model_metrics["auc"].append((model.model_name, model.auc))
            self.model_metrics["accuracy"].append((model.model_name, model.accuracy))
            self.model_metrics["precision"].append((model.model_name, model.precision))
            self.model_metrics["recall"].append((model.model_name, model.precision))
            self.model_metrics["f1"].append((model.model_name, model.f1))

    def _add_metric(self, model, metric):
        self.model_metrics[metric].append((model.model_name, getattr(model, metric)))

    def sort_metrics(self):
        """Sort saved metrics."""
        for metric in self.model_metrics:
            if metric in self.descending_metrics:
                self.model_metrics[metric].sort(
                    key=operator.itemgetter(1), reverse=True
                )
            else:
                self.model_metrics[metric].sort(key=operator.itemgetter(1))

    def print_sorted_metric(self, metric: str):
        """Print metrics in best to worst score order."""
        print(f"{metric}:")
        for index, result in enumerate(self.model_metrics[metric], start=1):
            print(f"{index}. {result[0]}: {result[1]}")

    def create_graph(self, metric: str):
        """Crate and display graph to compare saved models."""
        x_metric = [model_metric[0] for model_metric in self.model_metrics[metric]]

        if metric in ["train_time", "prediction_time"]:
            y_metric = [
                model_metric[1].microseconds
                for model_metric in self.model_metrics[metric]
            ]
        else:
            y_metric = [model_metric[1] for model_metric in self.model_metrics[metric]]

        sn.set(style="whitegrid")
        ax = sn.barplot(x=x_metric, y=y_metric)
        ax.tick_params(axis="x", rotation=90)
        ax.set_title(metric)
        plt.show()

    def print_results(self):
        """Print comparison of metrics."""
        for metric in self.model_metrics:
            self.print_sorted_metric(metric)
            self.create_graph(metric)

    def print_best(self):
        """Print best score for given metrics."""
        for metric in self.model_metrics:
            print(f"{metric}: {self.model_metrics[metric][0][0]}")
