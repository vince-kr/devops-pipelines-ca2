from . import config
from communication import persistence

def event_recorder(event_data: dict[str, str], testing=False):
    if not testing:
        try:
            persistence.persist_event(event_data, config.EVENT_RECORDS_PATH)
            return ""
        except FileNotFoundError as fe:
            return str(fe)
        except PermissionError as pe:
            return str(pe)
    else:
        return ""