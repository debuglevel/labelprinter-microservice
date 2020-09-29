from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import brother_ql
import logging
import logging.config
import app.print
import app.image
import app.health
import app.model
import app.label
import json

with open('logging-config.json', 'rt') as loggingConfigFile:
    loggingConfig = json.load(loggingConfigFile)
    logging.config.dictConfig(loggingConfig)

logger = logging.getLogger(__name__)


class AddPrintRequest(BaseModel):
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


class AddPrintResponse(BaseModel):
    label_width: int
    needed_resize: bool
    image_mimetype: str



fastapi = FastAPI()

@fastapi.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    logger.info("Sample INFO log message")
    logger.debug("Sample DEBUG log message")


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
async def post_prints(addPrintRequest: AddPrintRequest):
    """
    Add a printing job
    """
    logger.info("Got POST request on /prints/")

    # check if given printer model and label type are valid
    if app.model.is_valid(addPrintRequest.printer_model) == False:
        raise HTTPException(
            status_code=400,
            detail=f"printer model '{addPrintRequest.printer_model}' is invalid"
        )
    if app.label.is_valid(addPrintRequest.label_type) == False:
        raise HTTPException(
            status_code=400,
            detail=f"label type '{addPrintRequest.label_type}' is invalid")

    # download image to temporary file
    image_path, image_mimetype = app.image.download_image(
        addPrintRequest.image_url)

    # prepare image to be sent to a label printer (TODO: maybe that would be better placed in print_image() itself)
    label_width = app.label.get_width(addPrintRequest.label_type)
    prepared_image_path, is_resized = app.image.prepare_image(
        image_path, image_mimetype, label_width)

    # send image to printer
    status = app.print.print_image(
        image_path=prepared_image_path,
        printer_model=addPrintRequest.printer_model,
        label_type=addPrintRequest.label_type,
        printer_backend=addPrintRequest.printer_backend,
        printer_url=addPrintRequest.printer_url,
        red=addPrintRequest.red,
        low_quality=addPrintRequest.low_quality,
        high_dpi=addPrintRequest.high_dpi,
        compress=addPrintRequest.compress)

    addPrintResponse = AddPrintResponse(
        **{
            "needed_resize": is_resized,
            "image_mimetype": image_mimetype,
            "label_width": label_width
        })

    return addPrintResponse
