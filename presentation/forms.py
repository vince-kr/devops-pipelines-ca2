from wtforms import DateField, Form, SelectField

class SowForm(Form):
    date = DateField()
    crop = SelectField("Crop", choices=[("Cress", "crop-cress"), ])
    location = SelectField("Location", choices=[
        ("Kitchen", "kitchen")
    ])
    location_type = SelectField("Location type", choices=[
        ("Indoors window box", "indoors-window-box")
    ])