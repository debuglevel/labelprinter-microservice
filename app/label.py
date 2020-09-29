import brother_ql
import logging

logger = logging.getLogger(__name__)

def get_label_legacy_structures():
    """
    This is a slim variant of the legacy brother_ql.devicedependent interface: https://github.com/pklaus/brother_ql/blob/638b365d45421696e1c2cd26952093d68f87155b/brother_ql/devicedependent.py
    It only exists to ensure compatibility if brother_ql.devicedependent is removed.
    Callers should be adapted to the new interface.
    """
    label_type_specs = {}

    from brother_ql.labels import LabelsManager
    lm = LabelsManager()
    for label in lm.iter_elements():
        l = {}
        l['name'] = label.name
        l['kind'] = label.form_factor
        l['color'] = label.color
        l['tape_size'] = label.tape_size
        l['dots_total'] = label.dots_total
        l['dots_printable'] = label.dots_printable
        l['right_margin_dots'] = label.offset_r
        l['feed_margin'] = label.feed_margin
        l['restrict_printers'] = label.restricted_to_models
        label_type_specs[label.identifier] = l

    return label_type_specs

def get_width(label: str):
    """
    Get width (i.e. printable pixels) of a label type
    """
    logger.debug(f"Getting image width for '{label}' labels...")

    labels = get_label_legacy_structures()
    width = labels[label]["dots_printable"][0]

    logger.debug(f"Got image width for '{label}' labels: {width}")
    return width


def get_all():
    logger.debug(f"Getting all label types...")
    # TODO: use brother_ql.labels instead of deprecated brother_ql.devicedependent
    labels = get_label_legacy_structures()
    logger.debug(f"Got all label types")
    return labels


def is_valid(label: str):
    logger.debug(f"Checking if {label} is a supported label type...")
    is_supported = label in get_all()
    logger.debug(f"Checked if {label} is a supported label type: {is_supported}")
    return is_supported
