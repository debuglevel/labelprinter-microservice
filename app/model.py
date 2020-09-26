import brother_ql
import logging

logger = logging.getLogger(__name__)

def get_all():
    # TODO: use brother_ql.models instead of deprecated brother_ql.devicedependent
    return brother_ql.devicedependent.models