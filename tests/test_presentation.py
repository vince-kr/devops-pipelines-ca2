import unittest
from presentation import app, forms


class TestFlaskApplication(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_route_to_record_sow_activity_exists(self):
        self.assertTrue(self.client.get("/sow"))


class TestFlaskForms(unittest.TestCase):
    def test_sow_form(self):
        sow_form = forms.SowForm()
        expected = (
            ("date", "DateField"),
            ("crop", "SelectField"),
            ("location", "SelectField"),
            ("location_type", "SelectField"),
        )
        actual = tuple((field.name, field.type) for field in sow_form)
        self.assertEqual(expected, actual)