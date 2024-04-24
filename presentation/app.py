from flask import Flask

app = Flask(__name__)

@app.route("/sow")
def record_sow():
    return "Sow"