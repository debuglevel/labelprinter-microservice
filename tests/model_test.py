import pytest
import app.model


@pytest.mark.asyncio
async def test_list_models():
    """
    Tests that some printer models are returned
    """
    models = app.model.get_all()
    assert "QL-500" in models
    assert "QL-820NWB" in models


@pytest.mark.asyncio
async def test_is_valid():
    """
    Tests that a model is validated
    """
    assert app.model.is_valid("QL-500") == True
    assert app.model.is_valid("QL-820NWB") == True
    assert app.model.is_valid("invalid") == False
