import unittest

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


class TestQueryParserCropsAndActions(unittest.TestCase):
    """Extract crop and action data from a user query"""
    # Test retrieving crops from query
    # Logic for retrieving ACTIONS is identical
    def test_givenSetOfValidCrops_whenQueryContainsOneCrop_returnCrop(self):
        one_crop = nlp("How much cress did I sow last year?")
        expected = {"cress"}
        actual = application.retrieve_crop(one_crop)
        self.assertEqual(expected, actual)

    def test_givenSetOfValidCrops_whenQueryContainsTwoCrops_returnBoth(self):
        two_crops = nlp("How many beds have potatoes or broadbeans?")
        expected = {"potato", "broadbean"}
        actual = application.retrieve_crop(two_crops)
        self.assertEqual(expected, actual)

    def test_givenSetOfValidCrops_whenQueryContainsNoCrops_returnNone(self):
        no_crops = nlp("How much time did I spend on maintenance last month?")
        actual = application.retrieve_crop(no_crops)
        self.assertIsNone(actual)

class TestQueryParserDateRange(unittest.TestCase):
    """Extract date objects from user query"""
    def setUp(self):
        self.today = datetime.date.today()

    # Valid cases: one or two mentions of a date, all of which can be parsed
    # QueryDate.date_range exposes a valid tuple of start date, end date
    def test_givenQueryWithValidDate_thenQueryDateObjectIsTrue(self):
        valid_date_indication = nlp("How much cress did I sow last year?")
        query_date = application.QueryDate(valid_date_indication)
        self.assertTrue(query_date)

    def test_givenLastYear_thenReturnDateRangeOneOneToTwelveThirtyOne(self):
        last_year = nlp("How much cress did I sow last year?")
        year = self.today.year - 1
        expected = (
            datetime.date(year, 1, 1),
            datetime.date(year, 12, 31),
        )
        query_date = application.QueryDate(last_year)
        actual = query_date.date_range
        self.assertEqual(expected, actual)

    def test_givenLastMonth_thenReturnDateRangeYearMonthOneToYearMonthEnd(self):
        date_last_month = nlp("How much time did I spend on maintenance last month?")
        year = self.today.year
        month = self.today.month
        last_month = month - 1
        last_day = (
                datetime.date(year, month, 1) - datetime.timedelta(days=1)).day
        expected = (
            datetime.date(year, last_month, 1),
            datetime.date(year, last_month, last_day),
        )
        query_date = application.QueryDate(date_last_month)
        actual = query_date.date_range
        self.assertEqual(expected, actual)

    def test_givenNamedMonth_thenReturnDateRangeYearMonthOnetoYearMonthEnd(self):
        february = nlp("Did I plant pumpkins in February?")
        expected = (
            datetime.date(2024, 2, 1),
            datetime.date(2024, 2, 29),
        )
        query_date = application.QueryDate(february)
        actual = query_date.date_range
        self.assertEqual(expected, actual)

    def test_givenLastWeek_thenReturnDateRangeLastWeek(self):
        last_week = nlp("How many courgettes did I harvest last week?")
        year = self.today.year
        week = self.today.isocalendar().week - 1
        expected = (
            datetime.date.fromisocalendar(year, week, 1),
            datetime.date.fromisocalendar(year, week, 7),
        )
        query_date = application.QueryDate(last_week)
        actual = query_date.date_range
        self.assertEqual(expected, actual)

    # Not valid cases: no date entities, or existing entities cannot be parsed
    # QueryDate.warning exposes the issue found
    def test_givenQueryWithoutDates_thenQueryDateObjectIsFalse(self):
        no_dates = nlp("How many beds have potatoes or broadbeans?")
        query_date = application.QueryDate(no_dates)
        self.assertFalse(query_date)
        expected = ("This query does not contain any dates. "
                    "Please specify a date or date range.")
        actual = query_date.warning
        self.assertEqual(expected, actual)

    def test_givenQueryWithFutureDate_thenQueryDateObjectIsFalse(self):
        future_date = nlp("How many eggs are gathered next Thursday?")
        query_date = application.QueryDate(future_date)
        self.assertFalse(query_date)
        expected = ("Date reference \"next Thursday\" cannot be parsed as a date, "
                    "or represents a future date.")
        actual = query_date.warning
        self.assertEqual(expected, actual)

    def test_givenQueryWithTrickyDate_thenQueryDateObjectIsFalse(self):
        tricky_date = nlp("How many eggs were gathered on May Day?")
        query_date = application.QueryDate(tricky_date)
        self.assertFalse(query_date)
        expected = ("Date reference \"May Day\" cannot be parsed as a date, "
                    "or represents a future date.")
        actual = query_date.warning
        self.assertEqual(expected, actual)