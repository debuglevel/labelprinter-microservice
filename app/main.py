from fastapi import FastAPI
import brother_ql

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

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
@app.get("/printers/")
async def list_printers():
    pass

# list all created prints
@app.get("/prints/")
async def list_prints():
    pass

# get a print
@app.get("/prints/{item_id}")
async def get_print(item_id: int):
    pass

# add a printing job
@app.post("/prints/")
async def post_prints():
    pass

