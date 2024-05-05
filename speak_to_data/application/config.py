from pathlib import Path

EVENT_RECORDS_PATH = Path(__file__).parent.parent.parent / "data" / "events.csv"
MOCK_DATA_SMALL = (Path(__file__).parent.parent /
                   "tests" / "test_data" / "small_mock_data.csv")

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
