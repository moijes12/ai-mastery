from loguru import logger

from ..ml.pipeline import SupportFlowMLPipeline


class MLService:
    def __init__(self):
        self.pipeline = SupportFlowMLPipeline()
        self._trained = False

    async def ensure_trained(self):
        """Lazy load / train the model on first use"""
        if not self._trained:
            logger.info("🔄 First prediction request - Training ML models...")
            self.pipeline.train()
            self._trained = True
            logger.success("✅ ML Models are now ready!")

    async def predict(self, subject: str, description: str) -> dict:
        """Main prediction method"""
        await self.ensure_trained()
        result = self.pipeline.predict(subject, description)

        logger.info(f"Prediction made → Category: {result['category']}")
        return result


# Singleton instance
ml_service = MLService()
