import unittest

import dateparser
import datetime
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
        self.today = datetime.date.today()
        self.one_crop = nlp("How much cress did I sow last year?")
        self.two_crops = nlp("How many beds have potatoes or broadbeans?")
        self.no_crops = nlp("How much time did I spend on maintenance last month?")
        self.future_date = nlp(
            "How many eggs are gathered next Thursday?"
        )
        self.february = nlp("Did I plant pumpkins in February?")
        self.last_week = nlp("How many courgettes did I harvest last week?")

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

    def test_givenQueryWithValidDate_thenQueryDateObjectIsTrue(self):
        query_date = application.QueryDate(self.one_crop)
        self.assertTrue(query_date)

    def test_givenQueryWithoutDates_thenQueryDateObjectIsFalse(self):
        actual = application.QueryDate(self.two_crops)
        self.assertFalse(actual)

    def test_givenQueryWithFutureDate_thenQueryDateObjectIsFalse(self):
        actual = application.QueryDate(self.future_date)
        self.assertFalse(actual)

    def test_givenLastYear_thenReturnDateRangeOneOneToTwelveThirtyOne(self):
        year = self.today.year - 1
        expected = (
            datetime.date(year, 1, 1),
            datetime.date(year, 12, 31),
        )
        query_date = application.QueryDate(self.one_crop)
        actual = query_date.date_range
        self.assertEqual(expected, actual)

    def test_givenLastMonth_thenReturnDateRangeYearMonthOneToYearMonthEnd(self):
        year = self.today.year
        month = self.today.month
        last_month = month - 1
        last_day = (
                datetime.date(year, month, 1) - datetime.timedelta(days=1)).day
        expected = (
            datetime.date(year, last_month, 1),
            datetime.date(year, last_month, last_day),
        )
        query_date = application.QueryDate(self.no_crops)
        actual = query_date.date_range
        self.assertEqual(expected, actual)

    def test_givenNamedMonth_thenReturnDateRangeYearMonthOnetoYearMonthEnd(self):
        expected = (
            datetime.date(2024, 2, 1),
            datetime.date(2024, 2, 29),
        )
        query_date = application.QueryDate(self.february)
        actual = query_date.date_range
        self.assertEqual(expected, actual)

    def test_givenLastWeek_thenReturnDateRangeLastWeek(self):
        year = self.today.year
        week = self.today.isocalendar().week - 1
        expected = (
            datetime.date.fromisocalendar(year, week, 1),
            datetime.date.fromisocalendar(year, week, 7),
        )
        query_date = application.QueryDate(self.last_week)
        actual = query_date.date_range
        self.assertEqual(expected, actual)