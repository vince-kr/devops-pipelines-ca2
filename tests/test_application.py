import unittest

from application import events

class TestEventRecorder(unittest.TestCase):
    def test_givenValidDict_eventRecorderReturnsEmptyString(self):
        expected = ""
        actual = events.event_recorder({
            "crop": "cress",
            "location": "kitchen",
            "location_type": "indoors-window-box"
        })
        self.assertEqual(expected, actual)