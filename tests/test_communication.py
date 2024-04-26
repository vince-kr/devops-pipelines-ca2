import unittest

from communication import persistence
from presentation import forms

class TestPersistence(unittest.TestCase):
    def setUp(self):
        pass

    def test_givenInvalidPath_thenRaiseError(self):
        invalid_path = "not a path"
        with self.assertRaises(FileNotFoundError):
            persistence.persist_event({"mock": "dict"}, invalid_path)

    def test_givenValidPathButNoAuthorisation_thenRaiseError(self):
        forbidden_path = "/usr/bin/cat"
        with self.assertRaises(PermissionError):
            persistence.persist_event({"mock": "dict"}, forbidden_path)