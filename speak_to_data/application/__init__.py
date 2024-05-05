import csv
import json
import os
import spacy
from speak_to_data.application import (
    config, events, prepare_for_model, query_parser
)
from speak_to_data import communication
from speak_to_data.application.query_parser import QueryData

nlp = spacy.load("en_core_web_sm")
event_recorder = events.event_recorder

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

parse_query = query_parser.parse_query

def generate_request_object(query_data: QueryData) -> str:
    altered_query = query_data.crux
    dataset = communication.read_full_dataset(config.EVENT_RECORDS_PATH)
    altered_dataset = query_data

    return json.dumps({
        "query": altered_query,
        "table": altered_dataset,
        "options": {
            "wait_for_model": "true",
        },
    })
