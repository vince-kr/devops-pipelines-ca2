from speak_to_data import communication
from pathlib import Path

SECRETS_PATH = Path(__file__).parent.parent / "secret.json"
SECRETS = communication.read_json(SECRETS_PATH)
APP_DATA_PATH = Path(__file__).parent.parent / "app_data.json"
EVENT_RECORDS_PATH = Path(__file__).parent.parent.parent / "data" / "events.csv"
MOCK_DATA_DIR = Path(__file__).parent.parent / "tests" / "test_data"
MOCK_DATA_ONELINE = MOCK_DATA_DIR / "oneline_mock_data.csv"
MOCK_DATA_SMALL = MOCK_DATA_DIR / "small_mock_data.csv"
MOCK_DATA_LARGE = MOCK_DATA_DIR / "large_mock_data.csv"

FIELD_NAMES = [
    "date",
    "action",
    "crop",
    "quantity",
    "duration",
    "location",
    "location_type",
]

ACTION_NAMES = {
    "sow": [
        "date",
        "crop",
        "quantity",
        "location",
        "location_type",
    ],
    "maintain": [
        "date",
        "duration",
        "location",
        "location_type",
    ],
    "harvest": [
        "date",
        "crop",
        "quantity",
        "location",
        "location_type",
    ],
}

ACTIONS = set(communication.read_json(APP_DATA_PATH)["actions"])
CROPS = set(communication.read_json(APP_DATA_PATH)["crops"])
LOCATIONS = set(communication.read_json(APP_DATA_PATH)["locations"])

NOT_SAVED_WARNING = "Your data was not saved!"
