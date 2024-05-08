import datetime
from flask_wtf import FlaskForm
from wtforms import DateField, RadioField, SelectField, StringField
from wtforms_components import DateRange


class QueryForm(FlaskForm):
    user_query = StringField("User query")


class SowForm(FlaskForm):
    date = DateField(
        validators=[DateRange(
            max=datetime.date.today()
        )]
    )
    crop = SelectField(
        "Crop",
        choices=(
            ("cress", "Cress"),
            ("carrots", "Carrots"),
            ("pumpkins", "Pumpkins"),
        )
    )
    location = SelectField(
        "Location",
        choices=(
            ("kitchen", "Kitchen"),
            ("hoop-house-east", "Hoop house East"),
            ("hoop-house-west", "Hoop house West"),
            ("herb-garden", "Herb garden"),
        )
    )
    location_type = SelectField(
        "Location type",
        choices=(
            ("indoors-window-box", "Indoors window box"),
            ("outdoors-raised-bed", "Outdoors raised bed"),
            ("hoop-house-raised-bed", "Hoop house raised bed"),
        )
    )

class MaintainForm(FlaskForm):
    date = DateField(
        validators=[DateRange(
            max=datetime.date.today()
        )]
    )
    duration = RadioField(choices=(
        ("1", "Less than 30 minutes"),
        ("3", "Between 30 and 90 minutes"),
        ("6", "More than 90 minutes"),
    ))
    location = SelectField(
        "Location",
        choices=(
            ("kitchen", "Kitchen"),
            ("hoop-house-east", "Hoop house East"),
            ("hoop-house-west", "Hoop house West"),
            ("herb-garden", "Herb garden"),
        )
    )
    location_type = SelectField(
        "Location type",
        choices=(
            ("indoors-window-box", "Indoors window box"),
            ("outdoors-raised-bed", "Outdoors raised bed"),
            ("hoop-house-raised-bed", "Hoop house raised bed"),
        )
    )

class HarvestForm(FlaskForm):
    date = DateField(
        validators=[DateRange(
            max=datetime.date.today()
        )]
    )
    crop = SelectField(
        "Crop",
        choices=(
            ("cress", "Cress"),
            ("carrots", "Carrots"),
            ("pumpkins", "Pumpkins"),
        )
    )
    weight = StringField()
    location = SelectField(
        "Location",
        choices=(
            ("kitchen", "Kitchen"),
            ("hoop-house-east", "Hoop house East"),
            ("hoop-house-west", "Hoop house West"),
            ("herb-garden", "Herb garden"),
        )
    )
    location_type = SelectField(
        "Location type",
        choices=(
            ("indoors-window-box", "Indoors window box"),
            ("outdoors-raised-bed", "Outdoors raised bed"),
            ("hoop-house-raised-bed", "Hoop house raised bed"),
        )
    )

def get_type_of_action(self) -> str:
    return type(self).__name__[:-4].lower()
