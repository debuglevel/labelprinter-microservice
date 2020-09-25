from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from cairosvg import svg2png
#from str2bool import str2bool
import os
import brother_ql
import sys
import subprocess
import tempfile
import logging
import requests
import tempfile


class Print(BaseModel):
    image_url: str
    description: Optional[str] = None
    red: bool
    low_quality: bool
    high_dpi: bool
    compress: bool
    printer_url: str
    printer_model: str
    label_type: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# TODO: check if there's something better provided
@app.get("/health")
async def get_health():
    return {"status": "up"}

# list all models supported by brother_ql
@app.get("/models/")
async def list_models():
    # TODO: use brother_ql.models instead of deprecated  brother_ql.devicedependent
    return brother_ql.devicedependent.models

# list all labels supported by brother_ql
@app.get("/labels/")
async def list_labels():
    # TODO: use brother_ql.labels instead of deprecated brother_ql.devicedependent
    return brother_ql.devicedependent.label_type_specs

# list all defined printers
# TODO: no idea if we should do that or rely on a printer URL/label/etc defined in the prints request
@app.get("/printers/")
async def list_printers():
    raise NotImplementedError

# list all created prints
@app.get("/prints/")
async def list_prints():
    # TODO: list all prints ever made
    raise NotImplementedError

# get a print
@app.get("/prints/{item_id}")
async def get_print(item_id: int):
    # TODO: get data about a print
    raise NotImplementedError

# add a printing job
# TODO: define proper HTTP status code
@app.post("/prints/")
async def post_prints(print: Print):
    # TODO: check passed parameters (e.g. valid printer model and valid label type)
    # TODO: download image_url to temporary file
    image_path = download_image(print.image_url)
    # TODO: check if it's a PNG (maybe do not support SVG because the CairoSVG is just insane in it's size; although it would be nice as a SVG could be rasterized exactly for a label; alternative would be a rather closely coupled request to the other microservice which provides the PNG to provide a perfect sized PNG)
    prepare_image(image_path, width)
    # TODO: maybe check the PNG size to report back whether resizing was needed
    # TODO: save print data to a dictionary or an actual database
    # TODO: send PNG to printer via brother_ql
    print_image()
    # TODO: report back some data (id, size, needed resize, original data like label, model, etc). No idea if we should block. Maybe add a "blocking" attribute to JSON to choose that.
    return print
    #pass

def get_label_width(label: str):
    logging.debug(f"Getting image width for '{label}' labels...")
    labels = brother_ql.devicedependent.label_type_specs
    width = labels[label]["dots_printable"][0]
    logging.debug(f"Got image width for '{label}' labels: {width}")
    return width

def download_image(image_url: str):
    logging.debug(f'Downloading image {image_url}...')

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
    logging.debug(f'Converting SVG {svg_image_path} to PNG...')

    png_image_file = tempfile.NamedTemporaryFile(prefix='labelprinter_', suffix='.png', delete=False)
    png_image_path = png_image_file.name

    # TODO: output_width does not seem to work
    svg2png(open(svg_image_path, 'rb').read(), write_to=png_image_file, output_width=width)
    png_image_size = os.path.getsize(png_image_path)
    
    logging.debug(f'Converted {svg_image_path} to {png_image_path} with resulting size {png_image_size}')
    return png_image_path

def build_print_command(file_png_path: str, printer_model: str, label_type: str, printer_backend: str, printer_url: str, red: bool, low_quality: bool, high_dpi: bool, compress: bool):
    logging.debug(f'Building print command...')

    # Build command
    red_param = '--red' if red else None
    low_quality_param = '--lq' if low_quality else None
    high_dpi_param = '--600dpi' if high_dpi else None
    compress_param = '--compress' if compress else None

    # TODO: maybe call from library instead of subprocess
    # TODO: maybe brother_ql can read PIL Image instead of files; would prevent writing files
    command = ['/usr/bin/brother_ql', '--backend', printer_backend, '--model', printer_model, '--printer', printer_url, 'print', red_param, low_quality_param, high_dpi_param, compress_param, '--label', label_type, file_png_path]
    command = list(filter(None.__ne__, command)) # remove "None" from list

    logging.debug(f'Built print command: {command}')
    return command

def print_image(file_png_path: str, printer_model: str, label_type: str, printer_backend: str, printer_url: str, red: bool, low_quality: bool, high_dpi: bool, compress: bool):
    logging.debug(f'Printing image {file_png_path}...')

    command = build_print_command(file_png_path, printer_model, label_type, printer_backend, printer_url, red, low_quality, high_dpi, compress)

    # Run command
    logging.debug('Printing with following command: ...')
    logging.debug(command)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    logging.debug(result.stdout.decode('utf-8'))

    logging.debug(f'Printed image {file_png_path}')