import pytest
#from app.main import get_health
import app.main
import os.path
import PIL
import magic

@pytest.mark.asyncio
async def test_health():
    """
    Tests for some useful output on the /health endpoint (though only calling by python API)
    """
    status = (await app.main.get_health())["status"]
    assert status == "up"

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

@pytest.mark.asyncio
async def test_list_labels():
    """
    Tests that correct width for a label is returned
    """
    assert app.main.get_label_width("29x90") == 306
    assert app.main.get_label_width("62") == 696
