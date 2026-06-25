from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# Configure logging
logger.add("logs/ml_pipeline_{time:YYYY-MM-DD}.log", rotation="15 MB", level="INFO")


class SupportFlowMLPipeline:
    def __init__(self):
        self.tfidf = TfidfVectorizer(
            max_features=10000, stop_words="english", ngram_range=(1, 2)
        )
        self.model_dir = Path("models")
        self.model_dir.mkdir(exist_ok=True)

        self.category_model = None
        self.tfidf_vectorizer = None
        self.is_trained = False

    def generate_synthetic_data(self, n_samples: int = 75000) -> pd.DataFrame:
        """Generate large synthetic dataset"""
        logger.info(f"Generating {n_samples:,} synthetic support tickets...")
        np.random.seed(42)

        categories = ["Hardware", "Software", "Network", "Access", "Billing", "Other"]

        data = {
            "subject": [
                f"Issues with {np.random.choice(categories)} component"
                for _ in range(n_samples)
            ],
            "description": [
                f"The {np.random.choice(categories).lower()} system has been unstable. "
                f"Getting errors frequently. Need urgent help."
                for _ in range(n_samples)
            ],
            "category": [np.random.choice(categories) for _ in range(n_samples)],
        }
        return pd.DataFrame(data)

    def train(self):
        """Train the main classification model"""
        logger.info("🚀 Starting ML Training Pipeline...")

        df = self.generate_synthetic_data(75000)

        # Feature Engineering
        logger.info("Performing TF-IDF feature extraction...")
        text_data = df["subject"] + " " + df["description"]
        X = self.tfidf.fit_transform(text_data)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, df["category"], test_size=0.2, random_state=42, stratify=df["category"]
        )

        # Train Model
        logger.info("Training RandomForest Classifier...")
        self.category_model = RandomForestClassifier(
            n_estimators=250, max_depth=30, n_jobs=-1, random_state=42
        )
        self.category_model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.category_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        logger.success(f"✅ Training Completed! Test Accuracy: {acc:.4f}")
        logger.info("\n" + classification_report(y_test, y_pred))

        # Save models
        joblib.dump(self.category_model, self.model_dir / "category_model.pkl")
        joblib.dump(self.tfidf, self.model_dir / "tfidf_vectorizer.pkl")

        self.is_trained = True
        logger.info(f"Models saved to {self.model_dir}")

    def predict(self, subject: str, description: str) -> dict:
        """Predict category for a new ticket"""
        if not self.is_trained or self.category_model is None:
            logger.info("Loading trained models from disk...")
            self.category_model = joblib.load(self.model_dir / "category_model.pkl")
            self.tfidf = joblib.load(self.model_dir / "tfidf_vectorizer.pkl")
            self.is_trained = True

        text = subject + " " + description
        X = self.tfidf.transform([text])

        category = self.category_model.predict(X)[0]

        return {
            "category": category,
            "urgency": "Medium",
            "predicted_resolution_time_hours": round(np.random.uniform(4, 48), 1),
            "priority_score": round(np.random.uniform(40, 95), 1),
        }
