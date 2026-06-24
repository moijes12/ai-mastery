from loguru import logger
from app.ml.pipeline import SupportFlowMLPipeline


class MLService:
    def __init__(self):
        self.pipeline = SupportFlowMLPipeline()
        self._is_trained = False

    async def ensure_trained(self):
        """Lazy training on first request"""
        if not self._is_trained:
            logger.info("First prediction request - training models...")
            self.pipeline.train()
            self._is_trained = True
            logger.success("Models trained and ready!")

    async def predict_ticket(self, subject: str, description: str) -> dict:
        await self.ensure_trained()
        prediction = self.pipeline.predict(subject, description)
        return prediction


# Global instance
ml_service = MLService()
