import pytest
#from app.main import get_health
import app.health
import os.path
import PIL
import magic


@pytest.mark.asyncio
async def test_health():
    status = app.health.get_health().status
    assert status == "up"
