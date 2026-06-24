import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path
from loguru import logger

# Configure Loguru
logger.add("logs/supportflow_{time:YYYY-MM-DD}.log", rotation="10 MB", level="INFO")


class SupportFlowMLPipeline:
    def __init__(self):
        self.tfidf = TfidfVectorizer(max_features=8000, stop_words="english")
        self.model_dir = Path("models")
        self.model_dir.mkdir(exist_ok=True)

        self.category_model = None
        self.tfidf_vectorizer = None

    def generate_synthetic_data(self, n_samples: int = 60000) -> pd.DataFrame:
        """Generate realistic synthetic support tickets"""
        logger.info(f"Generating {n_samples:,} synthetic tickets...")

        np.random.seed(42)
        categories = ["Hardware", "Software", "Network", "Access", "Billing", "Other"]

        data = {
            "subject": [
                f"Problem with {np.random.choice(categories)} system"
                for _ in range(n_samples)
            ],
            "description": [
                f"My {np.random.choice(categories).lower()} has been having issues for the last few days. "
                f"It started suddenly and is affecting my work."
                for _ in range(n_samples)
            ],
            "category": [np.random.choice(categories) for _ in range(n_samples)],
        }

        return pd.DataFrame(data)

    def train(self):
        """Main training pipeline"""
        logger.info("🚀 Starting ML Training Pipeline...")

        df = self.generate_synthetic_data(60000)

        # Feature Engineering
        logger.info("Extracting TF-IDF features...")
        text_data = df["subject"] + " " + df["description"]
        X = self.tfidf.fit_transform(text_data)

        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, df["category"], test_size=0.2, random_state=42, stratify=df["category"]
        )

        # Train Model
        logger.info("Training RandomForest model...")
        self.category_model = RandomForestClassifier(
            n_estimators=200, random_state=42, n_jobs=-1
        )
        self.category_model.fit(X_train, y_train)

        # Evaluate
        train_acc = self.category_model.score(X_train, y_train)
        test_acc = self.category_model.score(X_test, y_test)

        logger.success("✅ Training completed!")
        logger.info(f"Train Accuracy: {train_acc:.4f} | Test Accuracy: {test_acc:.4f}")

        # Save models
        joblib.dump(self.category_model, self.model_dir / "category_model.pkl")
        joblib.dump(self.tfidf, self.model_dir / "tfidf_vectorizer.pkl")

        logger.info(f"Models saved to {self.model_dir}")

    def predict(self, subject: str, description: str) -> dict:
        """Predict for a single ticket"""
        if self.category_model is None:
            logger.info("Loading models from disk...")
            self.category_model = joblib.load(self.model_dir / "category_model.pkl")
            self.tfidf = joblib.load(self.model_dir / "tfidf_vectorizer.pkl")

        text = subject + " " + description
        X = self.tfidf.transform([text])

        category_pred = self.category_model.predict(X)[0]

        return {
            "category": category_pred,
            "urgency": "Medium",  # TODO: Add more models later
            "predicted_resolution_time_hours": 12.5,
            "priority_score": 72.0,
        }
