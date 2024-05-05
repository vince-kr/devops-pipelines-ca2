from speak_to_data import application, presentation

from flask import Flask, redirect, render_template

application.initial_setup()

app = Flask(__name__)
app.config["SECRET_KEY"] = "hush"


@app.route("/", methods=["GET", "POST"])
def index():
    form = presentation.QueryForm()
    if form.validate_on_submit():
        valid_query_data = application.parse_query(form.user_query)
        if valid_query_data:
            request_object = application.generate_request_object(valid_query_data)
            # Now use communication layer to call TaPas
        else:
            # Let the user know to change their query
            pass
    return render_template("index.html", form=form)

@app.route("/sow", methods=["GET", "POST"])
def record_sow():
    form = presentation.SowForm()
    if form.validate_on_submit():
        form_dict = dict((field.name, str(field.data)) for field in form)
        iso_date = f"{(d := form_dict['date'])[:4]}-{d[4:6]}-{d[6:8]}"
        form_dict["date"] = iso_date
        errors = application.event_recorder(form_dict)
        if not errors:
            return redirect("/")
    return render_template("sow.html", form=form)
