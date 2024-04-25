from flask import Flask, redirect, render_template, request
from . import forms

app = Flask(__name__)
app.config["SECRET_KEY"] = "hush"


@app.route("/")
def index():
    return "<h1>Speak to data</h1>"

@app.route("/sow", methods=["GET", "POST"])
def record_sow():
    form = forms.SowForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template("sow.html", form=form)
