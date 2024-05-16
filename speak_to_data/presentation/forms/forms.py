from speak_to_data.presentation.forms import action_form, shared_fields
from wtforms import StringField, IntegerField


class QueryForm(action_form.ActionForm):
    user_query = StringField("User query")


class SowForm(action_form.ActionForm):
    date = shared_fields.date
    crop = shared_fields.crop
    quantity = shared_fields.quantity
    location = shared_fields.location
    location_type = shared_fields.location_type


class MaintainForm(action_form.ActionForm):
    date = shared_fields.date
    duration = IntegerField("Duration in minutes")
    location = shared_fields.location
    location_type = shared_fields.location_type


class HarvestForm(action_form.ActionForm):
    date = shared_fields.date
    crop = shared_fields.crop
    quantity = shared_fields.quantity
    location = shared_fields.location
    location_type = shared_fields.location_type
