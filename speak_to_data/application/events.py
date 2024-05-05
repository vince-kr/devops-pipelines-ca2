from speak_to_data import application, communication

def event_recorder(event_data: dict[str, str], testing=False):
    if not testing:
        try:
            communication.persist_event(event_data,
                                        application.config.EVENT_RECORDS_PATH)
            return ""
        except FileNotFoundError as fe:
            return str(fe)
        except PermissionError as pe:
            return str(pe)
    else:
        return ""