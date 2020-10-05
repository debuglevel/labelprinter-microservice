from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
import subprocess
import logging
import os

logger = logging.getLogger(__name__)

BROTHER_QL_BACKEND = "API"
#BROTHER_QL_BACKEND = "command"


def build_print_command(image_path: str, printer_model: str, label_type: str,
                        printer_backend: str, printer_url: str, red: bool,
                        low_quality: bool, high_dpi: bool, compress: bool):
    """
    Builds a brother_ql CLI command line which can be run as a subprocess
    """
    logger.debug(f'Building print command...')

    # Build command
    red_param = '--red' if red else None
    low_quality_param = '--lq' if low_quality else None
    high_dpi_param = '--600dpi' if high_dpi else None
    compress_param = '--compress' if compress else None

    command = [
        'brother_ql', '--backend', printer_backend, '--model',
        printer_model, '--printer', printer_url, 'print', red_param,
        low_quality_param, high_dpi_param, compress_param, '--label',
        label_type, image_path
    ]
    command = list(filter(None.__ne__, command))  # remove "None" from list

    logger.debug(f'Built print command: {command}')
    return command


def run_print_command(command):
    """
    Runs the brother_ql printing command
    """
    logger.debug(f'Printing with following command: {command} ...')

    result = subprocess.run(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    logger.debug(result.stdout.decode('utf-8'))

    logger.debug(
        f"Printed with following command: {command}; result: {result}")


def call_print_api(image_path: str, printer_model: str, label_type: str,
                   printer_backend: str, printer_url: str, red: bool,
                   low_quality: bool, high_dpi: bool, compress: bool):
    """
    Prints an image by calling the brother_ql python API
    """
    logger.debug(f'Printing via brother_ql library...')

    raster = BrotherQLRaster(printer_model)
    raster.exception_on_warning = True

    high_quality = not low_quality
    threshold = 70
    rotate = "auto"
    cut = True
    dither = False
    image_paths = [image_path]
    logger.debug(f"Converting image {image_path} to printing instructions...")
    # TODO: maybe brother_ql can read PIL Image instead of files; would prevent writing files
    instructions = convert(qlr=raster,
                           images=image_paths,
                           label=label_type,
                           cut=cut,
                           dither=dither,
                           compress=compress,
                           red=red,
                           rotate=rotate,
                           dpi_600=high_dpi,
                           hq=high_quality,
                           threshold=threshold)
    logger.debug(
        f"Converted image {image_path} to printing instructions: {len(instructions)} bytes"
    )

    blocking = True
    logger.debug(f"Sending printing instructions to printer '{printer_url}' via '{printer_backend}' backend...")
    status = send(instructions=instructions,
                  printer_identifier=printer_url,
                  backend_identifier=printer_backend,
                  blocking=blocking)
    logger.debug(f"Sent printing instructions to printer '{printer_url}' via '{printer_backend}' backend: {status}")

    return status  # CAVEAT: network backend does not support readback according to brother_ql internals


def print_image(image_path: str, printer_model: str, label_type: str,
                printer_backend: str, printer_url: str, red: bool,
                low_quality: bool, high_dpi: bool, compress: bool):
    """
    Prints an image
    image_path can be basically every usual image format except SVG.
    """
    logger.debug(f'Printing image {image_path}...')

    if BROTHER_QL_BACKEND == "command":
        command = build_print_command(image_path, printer_model, label_type,
                                      printer_backend, printer_url, red,
                                      low_quality, high_dpi, compress)
        run_print_command(command)
    elif BROTHER_QL_BACKEND == "API":
        status = call_print_api(image_path, printer_model, label_type,
                                printer_backend, printer_url, red, low_quality,
                                high_dpi, compress)
    else:
        raise Exception("BROTHER_QL_BACKEND must be 'API' or 'command'")

    logger.debug(f'Printed image {image_path}')
    #return status
