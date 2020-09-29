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


def get_all():
    logger.debug(f"Getting all label types...")
    # TODO: use brother_ql.labels instead of deprecated brother_ql.devicedependent
    labels = brother_ql.devicedependent.label_type_specs
    logger.debug(f"Got all label types")
    return labels


def is_valid(label: str):
    logger.debug(f"Checking if {label} is a supported label type...")
    is_supported = label in get_all()
    logger.debug(f"Checked if {label} is a supported label type: {is_supported}")
    return is_supported
