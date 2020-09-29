import brother_ql
import logging

logger = logging.getLogger(__name__)


def get_model_legacy_structures():
    """
    This is a slim variant of the legacy brother_ql.devicedependent interface: https://github.com/pklaus/brother_ql/blob/638b365d45421696e1c2cd26952093d68f87155b/brother_ql/devicedependent.py
    It only exists to ensure compatibility if brother_ql.devicedependent is removed.
    Callers should be adapted to the new interface.
    """
    from brother_ql.models import ModelsManager
    models = []

    for model in ModelsManager().iter_elements():
        models.append(model.identifier)

    return models


def get_all():
    logger.debug(f"Getting all printer models...")
    # TODO: use brother_ql.models instead of deprecated brother_ql.devicedependent
    models = get_model_legacy_structures()
    logger.debug(f"Got all printer models")
    return models


def is_valid(model: str):
    logger.debug(f"Checking if {model} is a supported printer model...")
    is_supported = model in get_all()
    logger.debug(
        f"Checked if {model} is a supported printer model: {is_supported}")
    return is_supported
