import unittest

from speak_to_data import communication

class TestPersistence(unittest.TestCase):
    def setUp(self):
        pass

    def test_givenInvalidPath_thenRaiseError(self):
        invalid_path = "not a path"
        with self.assertRaises(FileNotFoundError):
            communication.persist_event({"mock": "dict"}, invalid_path)

    def test_givenValidPathButNoAuthorisation_thenRaiseError(self):
        forbidden_path = "/usr/bin/cat"
        with self.assertRaises(PermissionError):
            communication.persist_event({"mock": "dict"}, forbidden_path)