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