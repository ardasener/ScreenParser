from flask import Flask, request
from flask_cors import CORS
import logging
import cli
import os
import json


# Create flask app
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route("/hello", methods=['GET'])
def hello():
    return "hello"


@app.route("/run", methods=['POST'])
def run():
    images = request.json["input_files"]
    options = request.json["options"]

    returned =  cli.run(images, options)

    config = {"images": images, "options": options}
    config_path = os.path.join(returned["data_dir"], "config.json")
    config_file = open(config_path, "w+")
    json.dump(config, config_file, indent=2)
    config_file.close()

    return returned

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5111)