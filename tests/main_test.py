import pytest
import app.main

@pytest.mark.asyncio
async def test_list_models():
    """
    Tests that some printer models are returned
    """
    models = await app.main.list_models()
    assert "QL-500" in models
    assert "QL-820NWB" in models

@pytest.mark.asyncio
async def test_list_labels():
    """
    Tests that some label types are returned
    """
    labels = await app.main.list_labels()
    assert "62" in labels
    assert "29x90" in labels
