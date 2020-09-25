import brother_ql
import logging

logger = logging.getLogger(__name__)

def get_width(label: str):
    """
    Get width (i.e. printable pixels) of a label type
    """
    logger.debug(f"Getting image width for '{label}' labels...")

    labels = brother_ql.devicedependent.label_type_specs
    width = labels[label]["dots_printable"][0]
    
    logger.debug(f"Got image width for '{label}' labels: {width}")
    return width