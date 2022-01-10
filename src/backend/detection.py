import cv2
from screen_object import ScreenObject
import pickle
import sys
import easyocr
import os

def main(image_files, image_dir, cache_dir):
    all_objs = []
    for file in image_files:

        # INPUT

        # Get the filename from path (used for output files)
        filename = os.path.basename(file).split(".")[0]

        # Read the image
        image = cv2.imread(file)


        # EDGE DETECTION

        # Convert image to grayscale
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Blur the image to merge close objects together
        img_blur = cv2.GaussianBlur(img_gray,(5,5),1)

        # Binary thresholding (black and white image)
        ret, img_thres = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # Find contours
        contours, hierarchy = cv2.findContours(
            image=img_thres, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)


        # Get bounding boxes of contours and create the screen objects using them
        objs = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            x1, y1 = x, y
            x2 = x1 + w
            y2 = y1 + h

            obj = ScreenObject(x1, y1, x2, y2)
            objs.append(obj)

        # Create a copy of the image and draw the objs on it (GREEN)
        img_objs = image.copy()
        for obj in objs:
          x1,y1,x2,y2 = obj.get_xyxy()
          cv2.rectangle(img_objs, (x1,y1), (x2,y2), (0,255,0), 2)



        # OCR

        ocr_cache_file = os.path.join(cache_dir, filename + ".ocr.pickle")

        if os.path.exists(ocr_cache_file):
            file = open(ocr_cache_file, "rb")
            objs2 = pickle.load(file)
            file.close()
            objs += objs2
        else:
            reader = easyocr.Reader(['en'], gpu=False)

            results = reader.readtext(image)
            print(results)

            objs2 = []
            for points, text, confidence in results:
              if confidence > 0.6:
                x1 = int(points[0][0])
                x2 = int(points[1][0])
                y1 = int(points[0][1])
                y2 = int(points[3][1])
                obj = ScreenObject(x1, y1, x2, y2, text=text, confidence=confidence)
                objs2.append(obj)

            objs2 = [obj for obj in objs2 if len(obj.text) > 2]

            file = open(ocr_cache_file, "wb")
            pickle.dump(objs2, file)
            file.close()

            for obj in objs2:
              x1,y1,x2,y2 = obj.get_xyxy()
              cv2.rectangle(img_objs, (x1,y1), (x2,y2), (100,0,125), 2)

            objs += objs2


        # OUTPUT
        cv2.imwrite(os.path.join(image_dir, filename + ".detection.jpg"), img_objs)

        all_objs.append(objs)

    return all_objs