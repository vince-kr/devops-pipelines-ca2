import unittest
from presentation import app, forms


class TestFlaskApplication(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_route_to_record_sow_activity_exists(self):
        self.assertTrue(self.client.get("/sow"))


class TestFlaskForms(unittest.TestCase):
    def setUp(self):
        self.context = app.app.test_request_context()

    def test_sow_form(self):
        with self.context:
            sow_form = forms.SowForm()
        expected = (
            ("date", "DateField"),
            ("crop", "SelectField"),
            ("location", "SelectField"),
            ("location_type", "SelectField"),
            ("csrf_token", "CSRFTokenField"),
        )
        actual = tuple((field.name, field.type) for field in sow_form)
        self.assertEqual(expected, actual)

    def test_givenFormInstance_whenAskedOwnType_thenReturnsTypeAsString(self):
        with self.context:
            sow_form = forms.SowForm()
        expected = "sow"
        actual = sow_form.get_type_of_action()
        self.assertEqual(expected, actual)
