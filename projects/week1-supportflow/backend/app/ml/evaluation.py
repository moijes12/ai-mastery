import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from .pipeline import SupportFlowMLPipeline


def evaluate_model():
    pipeline = SupportFlowMLPipeline()
    pipeline.train()  # This will use the existing trained model if available

    # A test set for evaluation
    df = pipeline.generate_synthetic_data(20000)
    text_data = df["subject"] + " " + df["description"]
    X = pipeline.tfidf.transform(text_data)

    y_true = df["category"]
    y_pred = pipeline.category_model.predict(X)

    acc = accuracy_score(y_true, y_pred)

    logger.success(f"Final Model Accuracy: {acc:.4f}")
    logger.info("\n" + classification_report(y_true, y_pred))

    # Save confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix")
    plt.savefig("models/confusion_matrix.png")
    logger.info("Confusion matrix saved to models/confusion_matrix.png")

    return acc
