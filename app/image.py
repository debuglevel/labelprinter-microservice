import tempfile
import logging
import requests
from cairosvg import svg2png
import tempfile
import sys
import os

def download_image(image_url: str):
    """
    Download an image to a file
    """
    logging.debug(f'Downloading image {image_url}...')

    # TODO: NamedTemporaryFile is probably nicer
    temporarydirectory_path = tempfile.mkdtemp()
    image_path = f"{temporarydirectory_path}/file.svg"
    logging.debug(f'Downloading {image_url} to {image_path}...')

    headers = {'Accept': 'image/svg+xml'}
    response = requests.get(image_url, headers=headers)
    with open(image_path, 'wb') as image_file:
        image_file.write(response.content)

    file_size = os.path.getsize(image_path)

    logging.debug(f'Downloaded {image_url} to {image_path} ({file_size} bytes)')
    return image_path

def prepare_image(image_path: str, width: int):
    """
    Prepares an image for printing with brother_ql (i.e. converting, resizing).
    """
    logging.debug(f'Preparing image {image_path}...')

    if is_png == False:
        # TODO: convert if not a PNG (TODO: dont know whether it actually must be a PNG or just anything PIL can read)
        pass
    else:
        pass
    
    # TODO: resize if PNG/raster and not in correct dimensions
    raise NotImplementedError
    logging.debug(f'Prepared image {image_path}: {png_image_path}')
    return png_image_path

def convert_svg_to_png(svg_image_path: str, width: int):
    """
    Converts a SVG to a PNG file
    """
    logging.debug(f'Converting SVG {svg_image_path} to PNG...')

    png_image_file = tempfile.NamedTemporaryFile(prefix='labelprinter_', suffix='.png', delete=False)
    png_image_path = png_image_file.name

    # TODO: output_width does not seem to work
    svg2png(open(svg_image_path, 'rb').read(), write_to=png_image_file, output_width=width)
    png_image_size = os.path.getsize(png_image_path)
    
    logging.debug(f'Converted {svg_image_path} to {png_image_path} with resulting size {png_image_size}')
    return png_image_path