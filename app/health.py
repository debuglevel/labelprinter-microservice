from pydantic import BaseModel

logger = logging.getLogger(__name__)

class Health(BaseModel):
    status: str

def get_health():
    return Health(status="up")