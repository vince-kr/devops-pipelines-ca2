import csv
import os
from speak_to_data.application import config, events, query_parser

config = config
event_recorder = events.event_recorder
retrieve_crop = query_parser.retrieve_crop


def initial_setup():
    erp = config.EVENT_RECORDS_PATH
    if not os.path.isfile(erp):
        fieldnames = [
            "date",
            "crop",
            "location",
            "location_type",
        ]
        try:
            with open(erp, "w", newline="") as event_record:
                w = csv.DictWriter(event_record, fieldnames=fieldnames, dialect="unix")
                w.writeheader()
        except OSError:
            pass