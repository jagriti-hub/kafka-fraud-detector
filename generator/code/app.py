from flask import Flask
from generator import generator_api

app = Flask(__name__)

app.register_blueprint(generator_api)

if __name__ == "__main__":
    app.run(debug=True)