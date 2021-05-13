from flask import Flask, render_template, Response
from detector import detector_api

app = Flask(__name__)

app.register_blueprint(detector_api)

if __name__ == "__main__":
    app.run(debug=True)