import detection
import filtering
import postprocessing
import clustering
import os
import appdirs
import pathlib
import shutil
import tempfile
import random
import json
import sys


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



def run(images, config):
    try:
        for file in os.listdir(image_dir):
            path = os.path.join(image_dir, file)
            os.remove(path)

        for file in os.listdir(data_dir):
            if "pickle" not in file:
                path = os.path.join(data_dir, file)
                os.remove(path)

        run_id = int(random.getrandbits(32))

        print("Detection Stage...")
        all_objs = detection.main(images, image_dir, cache_dir, config["detection"], run_id)
        print("Filtering Stage...")
        all_objs = filtering.main(all_objs, images, image_dir, config["filtering"], run_id)
        print("Clustering Stage...")
        all_clusters = clustering.main(all_objs, images, image_dir, config["clustering"], run_id)
        print("PostProcessing Stage...")
        postprocessing.main(all_clusters, images, data_dir, image_dir, config["postprocessing"], run_id)



        return {"image_dir": image_dir, "data_dir": data_dir, "error": None}
    except Exception as ex:
        return {"image_dir": image_dir, "data_dir": data_dir, "error": str(ex)}

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Use: python cli.py config.json")
        sys.exit(1)
    else:
        config_file = open(sys.argv[1], "r")
        config = json.load(config_file)
        config_file.close()
        images = config["images"]
        options = config["options"]
        returned = run(images,options)
        if returned["error"] is not None:
            print("An error occurred!")
            print(returned["error"])
        else:
            print("Done!")
            print("Image Folder:", image_dir)
            print("Data Folder:", data_dir)
