import logging
import json
from flask import Flask, Response, request, render_template

import default_settings

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(default_settings)

from recommend import recommend_by_url


@app.route("/recommend")
def recommend():
    results = recommend_by_url(request.args.get('url'))
    data = json.dumps({'results': results})
    return Response(data, headers={'Content-Type': 'application/json'})


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5000)
