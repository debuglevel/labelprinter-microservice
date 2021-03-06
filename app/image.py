import tempfile
import logging
import requests
from cairosvg import svg2png
import tempfile
import sys
import os
from PIL import Image

logger = logging.getLogger(__name__)


def download_image(image_url: str):
    """
    Download an image to a file
    """
    logger.debug(f'Downloading image {image_url}...')

    image_file = tempfile.NamedTemporaryFile(prefix='labelprinter_',
                                             suffix='.downloaded',
                                             delete=False)

    logger.debug(f'Downloading {image_url} to {image_file.name}...')
    headers = {'Accept': 'image/svg+xml, image/png;q=0.9, image/*;q=0.8'}
    response = requests.get(image_url, headers=headers)
    image_file.write(response.content)
    image_file.close()

    image_mimetype = response.headers['content-type']
    file_size = os.path.getsize(image_file.name)

    logger.debug(
        f'Downloaded {image_url} to {image_file.name} ({file_size} bytes)')
    return image_file.name, image_mimetype


def prepare_image(image_path: str, image_mimetype: str, width: int):
    """
    Prepares an image for printing with brother_ql (i.e. converting, resizing).
    """
    image_size = os.path.getsize(image_path)
    logger.debug(f'Preparing image {image_path} ({image_size} bytes)...')

    if image_mimetype == "image/svg+xml":
        raster_image_path = convert_svg_to_png(image_path, width)
    else:
        raster_image_path = image_path

    resized_image_path, is_resized = resize_image(raster_image_path, width)

    resized_image_size = os.path.getsize(resized_image_path)
    logger.debug(
        f'Prepared image {image_path}: {resized_image_path} ({resized_image_size} bytes)'
    )
    return resized_image_path, is_resized


def resize_image(image_path: str, destination_width: int):
    """
    Resizes image if width is wrong.
    """
    logger.debug(
        f'Resizing image {image_path} to width={destination_width}...')

    # see https://stackoverflow.com/a/451580/4764279
    image = Image.open(image_path)
    image_width = float(image.size[0])

    if (image_width == destination_width):
        logger.debug(
            f"Image width {image_width}px is already destination width {destination_width}px. No resizing needed."
        )
        is_resized = False
        destination_image_path = image_path
    else:
        logger.debug(
            f"Image width {image_width}px is not destination width {destination_width}px. Resizing..."
        )
        is_resized = True

        destination_scaling = float(destination_width / image_width)
        image_height = float(image.size[1])
        destination_size = int(image_height * destination_scaling)
        resized_image = image.resize((destination_width, destination_size),
                                     Image.ANTIALIAS)

        resized_image_file = tempfile.NamedTemporaryFile(
            prefix='labelprinter_', suffix='.resized.png', delete=False)
        resized_image_path = resized_image_file.name
        resized_image.save(resized_image_path)

        destination_image_path = resized_image_path

    destination_image_size = os.path.getsize(destination_image_path)
    image_width, image_height = get_size(destination_image_path)
    logger.debug(
        f'Resized image {image_path} to width={destination_width}: (Width={image_width} Height={image_height}) {destination_image_path} ({destination_image_size} bytes)'
    )
    return destination_image_path, is_resized


def get_size(image_path: str):
    """
    Getting the size of an image as (width, height)-tuple
    """

    logger.debug(f'Getting size of {image_path}...')

    # see https://stackoverflow.com/a/451580/4764279
    image = Image.open(image_path)
    image_width, image_height = image.size

    logger.debug(f'Got size of {image_path}: Width={image_width}px Height={image_height}px')
    return image_width, image_height

def convert_svg_to_png(svg_image_path: str, width: int):
    """
    Converts a SVG to a PNG file
    """
    logger.debug(f'Converting SVG {svg_image_path} to PNG...')

    png_image_file = tempfile.NamedTemporaryFile(
        prefix='labelprinter_', suffix='converted_from_svg.png', delete=False)
    png_image_path = png_image_file.name

    # CAVEAT: output_width sometimes does not work (https://github.com/Kozea/CairoSVG/issues/164)
    svg2png(open(svg_image_path, 'rb').read(),
            write_to=png_image_file,
            output_width=width)
    png_image_file.close()  # needed, as svg2png does not seem to clsoe file

    png_image_size = os.path.getsize(png_image_path)
    logger.debug(
        f'Converted {svg_image_path} to {png_image_path} ({png_image_size} bytes)'
    )
    return png_image_path
