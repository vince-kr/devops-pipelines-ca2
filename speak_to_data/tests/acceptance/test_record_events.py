import datetime
from dataclasses import dataclass
import re
from typing import Type, Union

from speak_to_data import presentation
from speak_to_data.presentation.forms import ActionForm
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


class Test_REF1_DisplayFormFields(unittest.TestCase):
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
            RouteFormFields(
                route="/sow",
                patterns=(
                    "input_with_date_attr",
                    "select_with_name_crop",
                    "select_with_name_location",
                    "select_with_name_location_type",
                )
            ),
            RouteFormFields(
                route="/plant",
                patterns=(
                    "input_with_date_attr",
                    "select_with_name_crop",
                    "select_with_name_location",
                    "select_with_name_location_type",
                )
            ),
            RouteFormFields(
                route="/maintain",
                patterns=(
                    "input_with_date_attr",
                    "input_with_radio_attr",
                    "select_with_name_location",
                    "select_with_name_location_type",
                )
            ),
            RouteFormFields(
                route="/harvest",
                patterns=(
                    "input_with_date_attr",
                    "select_with_name_crop",
                    "input_with_text_attr",
                    "select_with_name_location",
                    "select_with_name_location_type",
                )
            ),
        )

        for test in route_form_tests:
            with self.subTest(msg=f"Checking form fields at route: {test.route}"):
                route_html = self.client.get(test.route).text
                self.assertTrue(all(
                    re.search(patterns[pattern], route_html)
                    for pattern in test.patterns
                ))


@dataclass
class FormInputValidation:
    route: str
    form: Type[ActionForm]
    form_data: dict[str, Union[datetime.date, str]]


class Test_REF2_ValidateInputs(unittest.TestCase):
    """
    Epic: Record Events (RE)
    Functional requirement: the system must validate -- both at the client side and the
    server side -- that data entered by the user is valid.
    """

    def setUp(self):
        self.app = presentation.flask_app
        self.app.config["WTF_CSRF_ENABLED"] = False

    def test_givenValidInputsPerForm_thenFormValidatesSuccessfully(self):
        valid_input_tests = (
            FormInputValidation(
                route="/sow",
                form=presentation.SowForm,
                form_data={
                    "date": datetime.date.today(),
                    "crop": "cress",
                    "location": "kitchen",
                    "location_type": "indoor-window-box",
                }
            ),
            FormInputValidation(
                route="/maintain",
                form=presentation.MaintainForm,
                form_data={
                    "date": datetime.date.today(),
                    "duration": "1",
                    "location": "kitchen",
                    "location_type": "indoor-window-box",
                }
            ),
            FormInputValidation(
                route="/harvest",
                form=presentation.HarvestForm,
                form_data={
                    "date": datetime.date.today(),
                    "crop": "cress",
                    "weight": "40gr",
                    "location": "kitchen",
                    "location_type": "indoor-window-box",
                }
            ),
        )

        for test in valid_input_tests:
            with self.subTest(msg=f"Testing valid inputs for route: {test.route}"):
                with self.app.test_request_context(
                    path=test.route,
                    method="POST",
                    data=test.form_data
                ):
                    form = test.form()
                    inputs_are_valid = form.validate()
                self.assertTrue(inputs_are_valid)


    def test_givenInvalidInputsPerForm_thenFormDoesNotValidate(self):
        invalid_input_tests = (
            FormInputValidation(
                route="/sow",
                form=presentation.SowForm,
                form_data={
                    "date": datetime.date(2038, 1, 20),
                    "crop": "not a crop!",
                    "location": "not a location!",
                    "location_type": "not a location type!",
                }
            ),
            FormInputValidation(
                route="/maintain",
                form=presentation.MaintainForm,
                form_data={
                    "date": datetime.date(2038, 1, 20),
                    "duration": "4",
                    "location": "not a location!",
                    "location_type": "not a location type!",
                }
            ),
            FormInputValidation(
                route="/harvest",
                form=presentation.HarvestForm,
                form_data={
                    "date": datetime.date(2038, 1, 20),
                    "crop": "not a crop!",
                    "weight": "40gr",
                    "location": "not a location!",
                    "location_type": "not a location type!",
                }
            ),
        )

        for test in invalid_input_tests:
            with self.subTest(msg=f"Testing invalid inputs for route: {test.route}"):
                with self.app.test_request_context(
                        path=test.route,
                        method="POST",
                        data=test.form_data
                ):
                    form = test.form()
                    inputs_are_invalid = not form.validate()
                    warnings = form.errors
                self.assertTrue(inputs_are_invalid)


class Test_REF3_PersistEventRecords(unittest.TestCase):
    """
    Epic: Record Events (RE)
    Functional requirement: the system must persist the data entered by the user such
    that it may be recalled later, including between restarts of the application.
    (RE-F3)
    """

    def test_givenValidEventRecord_thenWriteRecordToCsv(self):
        pass