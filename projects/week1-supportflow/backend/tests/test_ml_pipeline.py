from app.ml.pipeline import SupportFlowMLPipeline


def test_pipeline_creation():
    pipeline = SupportFlowMLPipeline()
    assert pipeline is not None


def test_synthetic_data_generation():
    pipeline = SupportFlowMLPipeline()
    df = pipeline.generate_synthetic_data(1000)
    assert len(df) == 1000
    assert "subject" in df.columns
    assert "category" in df.columns


def test_train_and_predict():
    pipeline = SupportFlowMLPipeline()
    pipeline.train()

    result = pipeline.predict(
        "My email is not working", "Cannot send or receive emails for the last 2 hours"
    )

    assert "category" in result
    assert result["category"] is not None
