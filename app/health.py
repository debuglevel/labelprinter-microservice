from pydantic import BaseModel

class Health(BaseModel):
    status: str

def get_health():
    return Health(status="up")