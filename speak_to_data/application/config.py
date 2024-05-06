from speak_to_data import communication
from pathlib import Path

SECRETS_PATH = Path(__file__).parent.parent / "secret.json"
EVENT_RECORDS_PATH = Path(__file__).parent.parent.parent / "data" / "events.csv"
MOCK_DATA_ONELINE = (Path(__file__).parent.parent /
                   "tests" / "test_data" / "oneline_mock_data.csv")
MOCK_DATA_SMALL = (Path(__file__).parent.parent /
                     "tests" / "test_data" / "small_mock_data.csv")

secrets = communication.read_json(SECRETS_PATH)

ACTIONS = {
    "sow",
    "plant",
    "harden off",
    "maintain",
    "harvest",
}

CROPS = {
    "cress",
    "carrot",
    "potato",
    "zucchini",
    "broadbean",
}
