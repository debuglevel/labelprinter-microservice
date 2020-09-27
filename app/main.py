from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import brother_ql
import logging
import app.print
import app.image
import app.health
import app.model
import app.label

logging.basicConfig(level=logging.DEBUG)
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
    printer_backend: str
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
    return app.model.get_all()


@fastapi.get("/labels/")
async def list_labels():
    """
    List all labels supported by brother_ql
    """
    logger.info("Got GET request on /labels/")
    return app.label.get_all()


@fastapi.post("/prints/")
async def post_prints(print: PrintRequest):
    """
    Add a printing job
    """
    logger.info("Got POST request on /prints/")

    # check if given printer model and label type are valid
    if app.model.is_valid(print.printer_model) == False:
        raise HTTPException(
            status_code=400,
            detail=f"printer model '{print.printer_model}' is invalid")
    if app.label.is_valid(print.label_type) == False:
        raise HTTPException(
            status_code=400,
            detail=f"label type '{print.label_type}' is invalid")

    # download image to temporary file
    image_path, image_mimetype = app.image.download_image(print.image_url)

    # prepare image to be sent to a label printer (TODO: maybe that would be better placed in print_image() itself)
    label_width = app.label.get_width(print.label_type)
    prepared_image_path, is_resized = app.image.prepare_image(image_path, image_mimetype,
                                                  label_width)

    # send image to printer
    status = app.print.print_image(image_path=prepared_image_path,
                                   printer_model=print.printer_model,
                                   label_type=print.label_type,
                                   printer_backend=print.printer_backend,
                                   printer_url=print.printer_url,
                                   red=print.red,
                                   low_quality=print.low_quality,
                                   high_dpi=print.high_dpi,
                                   compress=print.compress)
    # TODO: report back some data (size, needed resize, original size, new size, original data like label, model, etc). No idea if we should block. Maybe add a "blocking" attribute to JSON to choose that.
    return print
