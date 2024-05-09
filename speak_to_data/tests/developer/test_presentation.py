import unittest
from speak_to_data import presentation
from flask_wtf import FlaskForm


class TestFlaskApplication(unittest.TestCase):
    def setUp(self):
        self.client = presentation.flask_app.test_client()

    def test_route_to_record_sow_activity_exists(self):
        self.assertTrue(self.client.get("/sow"))


class TestFlaskForms(unittest.TestCase):
    @staticmethod
    def _get_form_fields(form: FlaskForm) -> set[tuple[str, str]]:
        return set((field.name, field.type) for field in form)

    def setUp(self):
        context = presentation.flask_app.test_request_context()
        with context:
            self.query_form_fields = self._get_form_fields(presentation.QueryForm())
            self.sow_form = presentation.SowForm()
            self.sow_form_fields = self._get_form_fields(self.sow_form)

    def test_query_form(self):
        expected = {
            ("user_query", "StringField"),
            ("csrf_token", "CSRFTokenField"),
        }
        actual = self.query_form_fields
        self.assertEqual(expected, actual)

    def test_sow_form(self):
        expected = {
            ("date", "DateField"),
            ("crop", "SelectField"),
            ("location", "SelectField"),
            ("location_type", "SelectField"),
            ("csrf_token", "CSRFTokenField")
        }
        actual = self.sow_form_fields
        self.assertEqual(expected, actual)

    def test_givenFormInstance_whenAskedOwnType_thenReturnsTypeAsString(self):
        expected = "sow"
        actual = self.sow_form.get_type_of_action()
        self.assertEqual(expected, actual)
