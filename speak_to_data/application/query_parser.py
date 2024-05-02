import dateparser
import datetime
from speak_to_data.application import config
from spacy.tokens.doc import Doc
from typing import Optional


def _retrieve_from_query(query: Doc, retrieve_from: set[str]) -> Optional[set[str]]:
    query_lemmas = set(token.lemma_ for token in query)
    intersection = retrieve_from & query_lemmas
    return intersection if len(intersection) > 0 else None


def retrieve_crop(query: Doc) -> Optional[set[str]]:
    return _retrieve_from_query(query, config.CROPS)


def retrieve_action(query: Doc) -> Optional[set[str]]:
    return _retrieve_from_query(query, config.ACTIONS)


class QueryDate:
    def __init__(self, query: Doc) -> None:
        self.todays_date: datetime.date = datetime.date.today()
        self.date_entities = [ent.text for ent in query.ents if ent.label_ == "DATE"]
        # Generator of all date_entities that can be converted to datetime objects
        datetime_objects = (datetime_object for entity in self.date_entities
                            if (datetime_object := dateparser.parse(entity)))
        # List of date objects that are not in the future
        self.date_objects = [date_object for dto in datetime_objects
                             if (date_object := dto.date()) < self.todays_date]

    def __bool__(self):
        """Valid query dates: one or two parse-able dates in a query"""
        return (1 <= len(self.date_entities) < 3 and
                1 <= len(self.date_objects) < 3)

    @property
    def _one_date(self) -> bool:
        return len(self.date_objects) == 1

    @property
    def _two_dates(self) -> bool:
        return len(self.date_objects) == 2

    @property
    def date_range(self) -> Optional[tuple[datetime.date, datetime.date]]:
        """Tuple of start date, end date for filtering events"""
        if not self:
            return None

        if self._one_date:
            return self._infer_date_range(*self.date_objects)
        elif self._two_dates:
            return self._compute_date_range(*self.date_objects)

    def _infer_date_range(
            self,
            target_date: datetime.date
    ) -> tuple[datetime.date, datetime.date]:
        days_offset: int = (self.todays_date - target_date).days
        if days_offset > 360:
            # Date range should span all of last calendar year
            last_year = self.todays_date.year - 1
            date_range = (
                datetime.date(last_year, 1, 1),
                datetime.date(last_year, 12, 31)
            )
        elif days_offset > 8:
            # Date range should span one calendar month
            year = target_date.year
            month = target_date.month
            last_day = (
                    datetime.date(year, month+1, 1) - datetime.timedelta(days=1)
            ).day
            date_range = (
                datetime.date(year, month, 1),
                datetime.date(year, month, last_day)
            )
        else:
            # Date range is about last week
            year = target_date.year
            week = target_date.isocalendar().week
            date_range = (
                datetime.date.fromisocalendar(year, week, 1),
                datetime.date.fromisocalendar(year, week, 7),
            )
        return date_range

    @staticmethod
    def _compute_date_range(
            start: datetime.date, end: datetime.date
    ) -> tuple[datetime.date, datetime.date]:
        pass