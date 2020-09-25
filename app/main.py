from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import brother_ql
import logging
import app.print
import app.image
import app.health
import app.label

logger = logging.getLogger(__name__)

class PrintRequest(BaseModel):
    image_url: str
    description: Optional[str] = None
    red: bool
    low_quality: bool
    high_dpi: bool
    compress: bool
    printer_url: str
    printer_model: str
    label_type: str

fastapi = FastAPI()

@fastapi.get("/")
async def root():
    logger.info("Got GET request on /")
    return {"message": "Hello, this is labelprinter-microservice :-)"}

@fastapi.get("/health")
async def get_health():
    logger.info("Got GET request on /health")
    return app.health.get_health()

@fastapi.get("/models/")
async def list_models():
    """
    List all models supported by brother_ql
    """
    logger.info("Got GET request on /models/")
    # TODO: use brother_ql.models instead of deprecated brother_ql.devicedependent
    return brother_ql.devicedependent.models

@fastapi.get("/labels/")
async def list_labels():
    """
    List all labels supported by brother_ql
    """
    logger.info("Got GET request on /labels/")
    # TODO: use brother_ql.labels instead of deprecated brother_ql.devicedependent
    return brother_ql.devicedependent.label_type_specs

@fastapi.get("/prints/")
async def list_prints():
    """
    List all created prints
    TODO: list all prints ever made
    """
    logger.info("Got GET request on /prints/")
    raise NotImplementedError

@fastapi.get("/prints/{item_id}")
async def get_print(item_id: int):
    """
    Get a print
    TODO: get data about a print
    """
    logger.info(f"Got GET request on /prints/{id}")
    raise NotImplementedError

@fastapi.post("/prints/")
async def post_prints(print: PrintRequest):
    """
    Add a printing job
    TODO: define proper HTTP status code
    """
    logger.info("Got POST request on /prints/")
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



