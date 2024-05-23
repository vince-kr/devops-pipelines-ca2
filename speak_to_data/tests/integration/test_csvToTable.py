from speak_to_data import application
from speak_to_data.application import config, prepare_for_model, query_parser
from speak_to_data.communication import read_dataset
import unittest


class TestCsvReaderToTableGenerator(unittest.TestCase):
    def setUp(self):
        self.sow_cress = query_parser.QueryData(
            "How much cress did I sow last year?"
        )
        self.harvest_sprouts = query_parser.QueryData(
            "How many Brussels sprouts did I harvest last year?"
        )

    def test_givenMockDataFromCsv_thenTransformToDictWithKeysValues(self):
        data_from_csv = read_dataset(config.MOCK_DATA_SMALL)
        expected = {
            "action": ["sow", "sow"],
            "crop": ["cress", "cress"],
            "quantity": ["1sqft", "2sqft"],
        }
        actual = prepare_for_model.generate_model_ready_dataset(
            data_from_csv, self.sow_cress
        )
        self.assertEqual(expected, actual)

    def test_givenMockDataFromCsv_thenGetAllRelevantLines(self):
        data_from_csv = read_dataset(config.MOCK_DATA_LARGE)
        expected = {
            "action": ["harvest", "harvest", "harvest", "harvest",],
            "crop": ["sprout", "sprout", "sprout", "sprout",],
            "quantity": ["600gr", "800gr", "800gr", "800gr",]
        }
        actual = prepare_for_model.generate_model_ready_dataset(
            data_from_csv, self.harvest_sprouts
        )
        self.assertEqual(expected, actual)

    def test_lookAtGenerateRequestObject(self):
        expected = {
            "inputs": {
                "query": "what is the sum of all quantities?",
                "table": {
                    "action": ["sow", "sow"],
                    "crop": ["cress", "cress"],
                    "quantity": ["1sqft", "2sqft"],
                },
            },
            "options": {
                "wait_for_model": "True",
                "use_cache": "False",
            },
        }
        actual = application.generate_request_object(
            self.sow_cress, application.config.MOCK_DATA_SMALL
        )
        self.assertEqual(expected, actual)
