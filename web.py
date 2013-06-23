import logging

from flask import Flask

import default_settings

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(default_settings)


@app.route("/")
def index():
    return "Hello, Bell!"


if __name__ == "__main__":
    app.run(port=5000)
