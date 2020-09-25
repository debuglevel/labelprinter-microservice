import pytest
import app.label

@pytest.mark.asyncio
async def test_get_width():
    """
    Tests that correct width for a label is returned
    """
    assert app.label.get_width("29x90") == 306
    assert app.label.get_width("62") == 696
