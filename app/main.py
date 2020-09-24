from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

import brother_ql

class Print(BaseModel):
    image_url: str
    description: Optional[str] = None

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
    pass

# list all created prints
@app.get("/prints/")
async def list_prints():
    # TODO: list all prints ever made
    pass

# get a print
@app.get("/prints/{item_id}")
async def get_print(item_id: int):
    # TODO: get data about a print
    pass

# add a printing job
# TODO: define proper HTTP status code
@app.post("/prints/")
async def post_prints(print: Print):
    # TODO: check passed parameters (e.g. valid printer model and valid label type)
    # TODO: download image_url to temporary file
    # TODO: check if it's a PNG (maybe do not support SVG because the CairoSVG is just insane in it's size; although it would be nice as a SVG could be rasterized exactly for a label; alternative would be a rather closely coupled request to the other microservice which provides the PNG to provide a perfect sized PNG)
    # TODO: maybe check the PNG size to report back whether resizing was needed
    # TODO: save print data to a dictionary or an actual database
    # TODO: send PNG to printer via brother_ql
    # TODO: report back some data (id, size, needed resize, original data like label, model, etc). No idea if we should block. Maybe add a "blocking" attribute to JSON to choose that.
    return print
    #pass

