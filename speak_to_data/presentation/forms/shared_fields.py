import datetime

from speak_to_data import application
from wtforms import DateField, SelectField
from wtforms_components import DateRange

app_data_loader = application.AppDataLoader(application.config.APP_DATA_PATH)

all_crops = app_data_loader.load_crops()
crop = SelectField(
        "Crop",
        choices=all_crops
)

all_locations = app_data_loader.load_locations()
location = SelectField(
    "Location",
    choices=all_locations
)

all_location_types = app_data_loader.load_location_types()
location_type = SelectField(
    "Location type",
    choices=all_location_types
)

date = DateField(
    validators=[DateRange(
        max=datetime.date.today()
    )]
)