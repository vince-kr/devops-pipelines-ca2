import datetime
from pathlib import Path
from speak_to_data import application, communication
import unittest


class TestPersistenceErrors(unittest.TestCase):
    def setUp(self):
        pass

    def test_givenInvalidPath_thenRaiseError(self):
        invalid_path = Path("not a path")
        with self.assertRaises(FileNotFoundError):
            communication.persist_event({"mock": "dict"}, invalid_path)

    def test_givenValidPathButNoAuthorisation_thenRaiseError(self):
        forbidden_path = Path("/usr/bin/cat")
        with self.assertRaises(PermissionError):
            communication.persist_event({"mock": "dict"}, forbidden_path)


class TestDatasetReader(unittest.TestCase):
    def test_givenPathToMockData_thenReturnDict(self):
        mock_data_path = application.config.MOCK_DATA_SMALL
        expected = [{
            "date": datetime.date(2023, 4, 21),
            "action": "sow",
            "crop": "cress",
            "quantity": "1sqft",
            "location": "kitchen",
            "location_type": "indoor-window-box",
        },]
        actual = communication.persistence.read_full_dataset(mock_data_path)
        self.assertEqual(expected, actual)