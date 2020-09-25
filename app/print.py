import subprocess
import logging

def build_print_command(file_png_path: str, printer_model: str, label_type: str, printer_backend: str, printer_url: str, red: bool, low_quality: bool, high_dpi: bool, compress: bool):
    """
    Builds a brother_ql CLI command line which can be run as a subprocess
    """
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

def run_print_command(command):
    """
    Runs the brother_ql printing command
    """
    logging.debug(f'Printing with following command: {command} ...')

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    logging.debug(result.stdout.decode('utf-8'))

    logging.debug(f'Printed with following command: {command}')

def print_image(file_png_path: str, printer_model: str, label_type: str, printer_backend: str, printer_url: str, red: bool, low_quality: bool, high_dpi: bool, compress: bool):
    """
    Prints an image
    """
    logging.debug(f'Printing image {file_png_path}...')

    command = build_print_command(file_png_path, printer_model, label_type, printer_backend, printer_url, red, low_quality, high_dpi, compress)
    run_print_command(command)

    logging.debug(f'Printed image {file_png_path}')