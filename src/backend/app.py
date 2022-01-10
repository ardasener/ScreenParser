from flask import Flask, request
import detection
import filtering
import postprocessing
import clustering
import os
import appdirs
import pathlib
import shutil
import tempfile


# Setup the directories where the data will be written
appname = "ScreenParser"
appauthor = "ardasener"
root_dir = appdirs.user_data_dir(appname, appauthor)
image_dir = os.path.join(root_dir, "images")
data_dir = os.path.join(root_dir, "data")
temp_dir = tempfile.gettempdir()
cache_dir = os.path.join(temp_dir, "screenparser", "cache")

pathlib.Path(image_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(cache_dir).mkdir(parents=True, exist_ok=True)



# Create flask app
app = Flask(__name__)


@app.route("/run", methods=['POST'])
def run():
    for file in os.listdir(image_dir):
        path = os.path.join(image_dir, file)
        os.remove(path)

    for file in os.listdir(data_dir):
        if "pickle" not in file:
            path = os.path.join(data_dir, file)
            os.remove(path)

    images = request.json["images"]
    app.logger.info(images)


    all_objs = detection.main(images, image_dir, cache_dir)
    all_objs = filtering.main(all_objs, images, image_dir)
    all_clusters = clustering.main(all_objs, images, image_dir)
    postprocessing.main(all_clusters, images, data_dir, image_dir)

    return {"image_dir": image_dir, "data_dir": data_dir}