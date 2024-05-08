from dataclasses import dataclass
import re
from speak_to_data import presentation
import unittest

"""
Unique per test:
- Route to get the source for
- Collection of patterns that should appear in the source
"""
@dataclass
class RouteFormFields:
    route: str
    patterns: tuple[str, ...]


class TestDisplayFormFields(unittest.TestCase):
    """
    Epic: Record Events (RE)
    Functional requirement: the system must present a browser UI displaying a form with
    fields pertaining to the event that the user wishes to record (RE-F1)
    """

    def setUp(self):
        self.client = presentation.flask_app.test_client()

    def test_correctFormFieldsAppearAtRecordRoutes(self):
        """Confirm that form fields with the expected attributes exist at each route"""
        patterns = {
            "input_with_date_attr": r'\<input[^\>]*type=\"date\"',
            "select_with_name_crop": r'\<select[^\>]*name=\"crop\"',
            "select_with_name_location": r'\<select[^\>]*name=\"location\"',
            "select_with_name_location_type": r'\<select[^\>]*name=\"location_type\"',
            "input_with_radio_attr": r'\<input[^\>]*type=\"radio\"',
            "input_with_text_attr":  r'\<input[^\>]*type=\"text\"',
        }

        route_form_tests = (
         RouteFormFields(route="/sow", patterns=(
            "input_with_date_attr",
            "select_with_name_crop",
            "select_with_name_location",
            "select_with_name_location_type",
        )),
         RouteFormFields(route="/plant", patterns=(
            "input_with_date_attr",
            "select_with_name_crop",
            "select_with_name_location",
            "select_with_name_location_type",
        )),
        RouteFormFields(route="/maintain", patterns=(
            "input_with_date_attr",
            "input_with_radio_attr",
            "select_with_name_location",
            "select_with_name_location_type",
        )),
        RouteFormFields(route="/harvest", patterns=(
            "input_with_date_attr",
            "select_with_name_crop",
            "input_with_text_attr",
            "select_with_name_location",
            "select_with_name_location_type",
        )),
        )

        for form in route_form_tests:
            with self.subTest(msg=f"Checking form fields at route: {form.route}"):
                route_html = self.client.get(form.route).text
                self.assertTrue(all(
                    re.search(patterns[pattern], route_html)
                    for pattern in form.patterns
                ))