from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import brother_ql
import logging
import app.print
import app.image

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

@app.get("/health")
async def get_health():
    """
    TODO: check if there's something better provided
    """
    return {"status": "up"}

@app.get("/models/")
async def list_models():
    """
    List all models supported by brother_ql
    """
    # TODO: use brother_ql.models instead of deprecated  brother_ql.devicedependent
    return brother_ql.devicedependent.models

@app.get("/labels/")
async def list_labels():
    """
    List all labels supported by brother_ql
    """
    # TODO: use brother_ql.labels instead of deprecated brother_ql.devicedependent
    return brother_ql.devicedependent.label_type_specs

@app.get("/printers/")
async def list_printers():
    """
    List all defined printers
    TODO: no idea if we should do that or rely on a printer URL/label/etc defined in the prints request
    """
    raise NotImplementedError

@app.get("/prints/")
async def list_prints():
    """
    List all created prints
    TODO: list all prints ever made
    """
    raise NotImplementedError

@app.get("/prints/{item_id}")
async def get_print(item_id: int):
    """
    Get a print
    TODO: get data about a print
    """
    raise NotImplementedError

@app.post("/prints/")
async def post_prints(print: Print):
    """
    Add a printing job
    TODO: define proper HTTP status code
    """
    # TODO: check passed parameters (e.g. valid printer model and valid label type)
    # TODO: download image_url to temporary file
    image_path, image_mimetype = download_image(print.image_url)
    
    prepare_image(image_path, image_mimetype, width)
    # TODO: maybe check the image size to report back whether resizing was needed
    # TODO: save print data to a dictionary or an actual database
    # TODO: send image to printer via brother_ql
    print.print_image()
    # TODO: report back some data (id, size, needed resize, original data like label, model, etc). No idea if we should block. Maybe add a "blocking" attribute to JSON to choose that.
    return print
    #pass

def get_label_width(label: str):
    """
    Get width (i.e. printable pixels) of a label type
    """
    logging.debug(f"Getting image width for '{label}' labels...")
    labels = brother_ql.devicedependent.label_type_specs
    width = labels[label]["dots_printable"][0]
    logging.debug(f"Got image width for '{label}' labels: {width}")
    return width



