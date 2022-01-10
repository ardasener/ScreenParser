import os

def find_image(data_file, image_dir):
    filename = os.path.basename(data_file).split(".")[0].strip()

    for image in os.listdir(image_dir):
        image_filename = os.path.basename(image).split(".")[0].strip()
        if filename == image_filename:
            return os.path.join(image_dir, image)