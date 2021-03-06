import pytest
import app.image
import os.path
import PIL
import magic


@pytest.mark.skip(reason="slow and needs connectivity")
@pytest.mark.asyncio
async def test_download_image():
    """
    Tests that an image is downloaded
    """
    image_path, image_mimetype = app.image.download_image(
        "https://upload.wikimedia.org/wikipedia/commons/c/c3/Resistor_symbol_IEC.svg"
    )
    assert os.path.exists(image_path) == True
    assert os.path.getsize(image_path) > 0


@pytest.mark.asyncio
async def test_prepare_image():
    """
    Tests that images are prepared correctly
    """
    for image_path in [
            "tests/resources/image.svg", "tests/resources/image_large.png",
            "tests/resources/image_small.png",
            "tests/resources/image_large.gif",
            "tests/resources/image_large.jpg",
            "tests/resources/image_large.webp",
            "tests/resources/image_large.bmp"
    ]:
        #print(f"Current: {image_path}")
        mimetype = "image/svg+xml" if image_path.endswith(
            ".svg") else "image/*"
        prepared_image_path, is_resized = app.image.prepare_image(
            image_path, mimetype, 100)
        assert os.path.exists(prepared_image_path)
        assert os.path.getsize(prepared_image_path) > 0

        image = PIL.Image.open(prepared_image_path)
        width, height = image.size
        assert width == 100


@pytest.mark.asyncio
async def test_resize_image():
    """
    Tests that rastered images are resized correctly
    """
    for image_path in [
            "tests/resources/image_large.png",
            "tests/resources/image_small.png",
            "tests/resources/image_large.gif",
            "tests/resources/image_large.jpg",
            "tests/resources/image_large.webp",
            "tests/resources/image_large.bmp"
    ]:
        #print(f"Current: {image_path}")
        resized_image_path, is_resized = app.image.resize_image(
            image_path, 100)
        assert is_resized == True
        assert os.path.exists(resized_image_path)
        assert os.path.getsize(resized_image_path) > 0

        image = PIL.Image.open(resized_image_path)
        width, height = image.size
        assert width == 100


@pytest.mark.asyncio
async def test_resize_image_not_needed():
    """
    Tests that rastered images in correct dimensions are not resized
    """
    for image_path in ["tests/resources/image.png"]:
        #print(f"Current: {image_path}")
        resized_image_path, is_resized = app.image.resize_image(
            image_path, 100)
        assert is_resized == False
        assert os.path.exists(resized_image_path)
        assert os.path.getsize(resized_image_path) > 0

        image = PIL.Image.open(resized_image_path)
        width, height = image.size
        assert width == 100


@pytest.mark.skip(reason="fixed width conversion does not work")
@pytest.mark.asyncio
async def test_convert_svg_to_png():
    """
    Tests that SVG is converted to PNG
    """
    png_image_path = app.main.convert_svg_to_png("tests/resources/image.svg",
                                                 100)
    assert os.path.exists(png_image_path)
    assert os.path.getsize(png_image_path) > 0

    mime_type = magic.from_file(png_image_path, mime=True)
    assert mime_type == "image/png"

    image = PIL.Image.open(png_image_path)
    width, height = image.size
    assert width == 100
