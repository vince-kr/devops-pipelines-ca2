import unittest

from speak_to_data import application
import spacy

nlp = spacy.load("en_core_web_sm")


class TestEventRecorder(unittest.TestCase):
    def test_givenValidDict_eventRecorderReturnsEmptyString(self):
        expected = ""
        actual = application.event_recorder({
            "crop": "cress",
            "location": "kitchen",
            "location_type": "indoors-window-box"
        })
        self.assertEqual(expected, actual)


class TestQueryParser(unittest.TestCase):
    def setUp(self):
        self.one_crop = nlp("How much cress did I sow last year?")
        self.two_crops = nlp("How many beds have potatoes or broadbeans?")
        self.no_crops = nlp("The rain in Spain falls mainly on the Spaniards")

    # Test retrieving crops from query
    # Logic for retrieving ACTIONS is identical
    def test_givenSetOfValidCrops_whenQueryContainsOneCrop_returnCrop(self):
        expected = {"cress"}
        actual = application.retrieve_crop(self.one_crop)
        self.assertEqual(expected, actual)

    def test_givenSetOfValidCrops_whenQueryContainsTwoCrops_returnBoth(self):
        expected = {"potato", "broadbean"}
        actual = application.retrieve_crop(self.two_crops)
        self.assertEqual(expected, actual)

    def test_givenSetOfValidCrops_whenQueryContainsNoCrops_returnNone(self):
        actual = application.retrieve_crop(self.no_crops)
        self.assertIsNone(actual)
