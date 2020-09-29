import brother_ql
import logging

logger = logging.getLogger(__name__)


def get_all():
    logger.debug(f"Getting all printer models...")
    # TODO: use brother_ql.models instead of deprecated brother_ql.devicedependent
    models = brother_ql.devicedependent.models
    logger.debug(f"Got all printer models")
    return models


def is_valid(model: str):
    logger.debug(f"Checking if {model} is a supported printer model...")
    is_supported = model in get_all()
    logger.debug(f"Checked if {model} is a supported printer model: {is_supported}")
    return is_supported
