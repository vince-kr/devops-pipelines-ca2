import csv
import os

def persist_event(event_data: dict[str, str], persistence_path: str) -> None:
    if not os.path.isfile(persistence_path):
        raise FileNotFoundError(
            f"Trying to store the record at {persistence_path}"
            f"but this is not a valid path."
        )
    fieldnames = list(event_data.keys())
    try:
        with open(persistence_path, "a") as events_store:
            w = csv.DictWriter(events_store, fieldnames=fieldnames, dialect="unix")
            w.writerow(event_data)
    except PermissionError as pe:
        raise PermissionError(f"Not allowed to write to file {pe.filename}")
