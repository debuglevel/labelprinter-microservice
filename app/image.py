import tempfile
import logging
import requests
from cairosvg import svg2png
import tempfile
import sys
import os
from PIL import Image

def download_image(image_url: str):
    """
    Download an image to a file
    """
    logging.debug(f'Downloading image {image_url}...')

    image_file = tempfile.NamedTemporaryFile(prefix='labelprinter_', suffix='.downloaded', delete=False)
    logging.debug(f'Downloading {image_url} to {image_path.name}...')

    headers = {'Accept': 'image/svg+xml, image/png;q=0.9, image/*;q=0.8'}
    response = requests.get(image_url, headers=headers)
    image_file.write(response.content)
    image_file.close()

    image_mimetype = response.headers['content-type']
    file_size = os.path.getsize(image_path.name)

    logging.debug(f'Downloaded {image_url} to {image_path.name} ({file_size} bytes)')
    return image_path.name, image_mimetype

def prepare_image(image_path: str, image_mimetype: str, width: int):
    """
    Prepares an image for printing with brother_ql (i.e. converting, resizing).
    """
    logging.debug(f'Preparing image {image_path}...')

    if image_mimetype == "image/svg+xml":
        raster_image_path = convert_svg_to_png(image_path, width)
    else:
        raster_image_path = image_path

    resized_image_path = resize_image(raster_image_path, width)

    logging.debug(f'Prepared image {image_path}: {resized_image_path}')
    return resized_image_path

def resize_image(image_path: str, destination_width: int):
    """
    Resizes image if width is wrong.
    """
    logging.debug(f'Resizing image {image_path} to width={destination_width}...')

    image = Image.open(image_path)
    wpercent = (destination_width / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((destination_width, hsize), Image.ANTIALIAS)
    
    image_file = tempfile.NamedTemporaryFile(prefix='labelprinter_', suffix='.resized.png', delete=False)
    resized_image_path = image_file.name
    image.save(resized_image_path)

    logging.debug(f'Resized image {image_path} to width={destination_width}: {resized_image_path}')
    return resized_image_path

def convert_svg_to_png(svg_image_path: str, width: int):
    """
    Converts a SVG to a PNG file
    """
    logging.debug(f'Converting SVG {svg_image_path} to PNG...')

    png_image_file = tempfile.NamedTemporaryFile(prefix='labelprinter_', suffix='.png', delete=False)
    png_image_path = png_image_file.name

    # CAVEAT: output_width sometimes does not work (https://github.com/Kozea/CairoSVG/issues/164)
    svg2png(open(svg_image_path, 'rb').read(), write_to=png_image_file, output_width=width)
    png_image_size = os.path.getsize(png_image_path)
    
    logging.debug(f'Converted {svg_image_path} to {png_image_path} with resulting size {png_image_size}')
    return png_image_path