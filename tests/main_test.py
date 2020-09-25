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

@pytest.mark.skip(reason="slow")
@pytest.mark.asyncio
async def test_download_image():
    """
    Tests that an image is downloaded
    """
    image_path = app.main.download_image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Resistor_symbol_IEC.svg")
    assert os.path.exists(image_path)
    assert os.path.getsize(image_path) > 0

@pytest.mark.skip(reason="not yet implemented")
@pytest.mark.asyncio
async def test_prepare_image():
    """
    Tests that images are prepared correctly
    """
    for image_path in ["image.png", "image.svg", "image.gif", "image.jpg"]:
        png_image_path = app.main.prepare_image(image_path, 100)
        assert os.path.exists(png_image_path)
        assert os.path.getsize(png_image_path) > 0

        image = PIL.Image.open(png_image_path)
        width, height = image.size
        assert width == 100
        assert image_is_png # TODO: only if needed and no other raster images work

@pytest.mark.skip(reason="fixed width conversion does not work")
@pytest.mark.asyncio
async def test_convert_svg_to_png():
    """
    Tests that SVG is converted to PNG
    """
    png_image_path = app.main.convert_svg_to_png("tests/image.svg", 100)
    assert os.path.exists(png_image_path)
    assert os.path.getsize(png_image_path) > 0

    mime_type = magic.from_file(png_image_path, mime=True)
    assert mime_type == "image/png"

    image = PIL.Image.open(png_image_path)
    width, height = image.size
    assert width == 100