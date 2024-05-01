from pathlib import Path

EVENT_RECORDS_PATH = Path(__file__).parent.parent / "events.csv"

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
