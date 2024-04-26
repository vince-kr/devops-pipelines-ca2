import application
from application import events

from flask import Flask, redirect, render_template
from . import forms

application.initial_setup()

app = Flask(__name__)
app.config["SECRET_KEY"] = "hush"


@app.route("/")
def index():
    return "<h1>Speak to data</h1>"

@app.route("/sow", methods=["GET", "POST"])
def record_sow():
    form = forms.SowForm()
    if form.validate_on_submit():
        form_dict = dict((field.name, str(field.data)) for field in form)
        errors = events.event_recorder(form_dict)
        if not errors:
            return redirect("/")
    return render_template("sow.html", form=form)
