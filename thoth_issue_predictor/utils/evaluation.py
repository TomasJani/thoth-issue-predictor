import itertools
import operator

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
)

models_metrics = {
    "train_time": [],
    "number_of_errors": [],
    "auc": [],
    "accuracy_score": [],
    "f1 weighted": [],
    "f1 micro": [],
    "f1 macro": [],
}


def plot_confusion_matrix(
    cm, target_names, title="Confusion matrix", cmap=None, normalize=True
):
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap("Blues")

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(
                j,
                i,
                "{:0.4f}".format(cm[i, j]),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
            )
        else:
            plt.text(
                j,
                i,
                "{:,}".format(cm[i, j]),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
            )

    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel(
        "Predicted label\naccuracy={:0.4f}; misclass={:0.4f}".format(accuracy, misclass)
    )
    plt.show()


def sort_each_metric_best_to_worst(metrics):
    for metric in metrics:
        if metric in ["accuracy_score", "auc", "f1 weighted", "f1 micro", "f1 macro"]:
            metrics[metric].sort(key=operator.itemgetter(1), reverse=True)
        else:
            metrics[metric].sort(key=operator.itemgetter(1))


def numbers_for_given_metric(metrics, metric):
    print(f"{metric}:")
    for index, result in enumerate(metrics[metric], start=1):
        print(f"{index}. {result[0]}: {result[1]}")


def graph_for_given_metric(metrics, metric):
    x_metric = [model_metric[0] for model_metric in metrics[metric]]

    if metric == "train_time":
        y_metric = [model_metric[1].microseconds for model_metric in metrics[metric]]
    else:
        y_metric = [model_metric[1] for model_metric in metrics[metric]]

    sn.set(style="whitegrid")
    ax = sn.barplot(x=x_metric, y=y_metric)
    ax.tick_params(axis="x", rotation=90)
    ax.set_title(metric)
    plt.show()


def print_results(metrics):
    for metric in metrics:
        numbers_for_given_metric(metrics, metric)
        graph_for_given_metric(metrics, metric)
    print()


def best_in_each_category(metrics):
    for metric in metrics:
        print(f"{metric}: {metrics[metric][0][0]}")


def save_metrics(metrics, model_name, start, end, y_true, y_pred, n_errors):
    metrics["train_time"].append((model_name, end - start))
    metrics["number_of_errors"].append((model_name, n_errors))
    metrics["auc"].append((model_name, roc_auc_score(y_true, y_pred)))
    metrics["accuracy_score"].append((model_name, accuracy_score(y_true, y_pred)))
    metrics["f1 weighted"].append(
        (model_name, f1_score(y_true, y_pred, average="weighted"))
    )
    metrics["f1 micro"].append((model_name, f1_score(y_true, y_pred, average="micro")))
    metrics["f1 macro"].append((model_name, f1_score(y_true, y_pred, average="macro")))


# Function to represent comparable metrics
def print_metrics(start, end, y_true, y_pred, n_errors):
    print(f"Train time: {end - start}")
    print(f"Number of errors: {n_errors}")
    print(f"AUC: {roc_auc_score(y_true, y_pred)}")
    print(f"Accuracy Score: {accuracy_score(y_true, y_pred)}")
    print(f"F1 weighted: {f1_score(y_true, y_pred, average='weighted')}")
    print(f"F1 micro: {f1_score(y_true, y_pred, average='micro')}")
    print(f"F1 macro: {f1_score(y_true, y_pred, average='macro')}")

    print(classification_report(y_true, y_pred))
    cm = confusion_matrix(y_true, y_pred)
    print(cm)
    plot_confusion_matrix(cm, ["True", "False"], normalize=False)


def save_and_print_metrics(metrics, model_name, start, end, y_true, y_pred):
    n_errors = (y_pred != y_true).sum()
    save_metrics(metrics, model_name, start, end, y_true, y_pred, n_errors)
    print_metrics(start, end, y_true, y_pred, n_errors)
