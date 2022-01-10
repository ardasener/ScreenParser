import cv2
import easyocr
import numpy as np
import itertools
import random
from sklearn import cluster
from sklearn.preprocessing import Normalizer
from collections import Counter
from copy import deepcopy
import sys
import os
import pickle


image_file = sys.argv[1]
data_dir = sys.argv[2]
image_dir = sys.argv[3]

image_filename = os.path.basename(image_file).split(".")[0]

image = cv2.imread(image_file)  # Read image
cv2.imwrite(os.path.join(image_dir, image_filename + ".raw.jpg"), image)

class ScreenObject:
    def __init__(self, x1, y1, x2, y2, confidence=0.1, text=""):
        # Coordinates for the bounding box
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        # Float from 0 to 1
        # High confidence indicates the object
        # is more likely to be a correct detection
        self.confidence = confidence

        # Text detected by tesseract
        # If empty then the object contains no text
        self.text = text

        self.dists = []

    def get_center(self):
      return int(self.x1 + self.width()/2), int(self.y1 + self.height()/2)

    def get_xyxy(self):
        return self.x1, self.y1, self.x2, self.y2

    def get_xywh(self):
        return self.x1, self.y1, self.width(), self.height()

    def width(self):
        return self.x2 - self.x1

    def height(self):
        return self.y2 - self.y1

    def area(self):
        return self.width() * self.height()

    def horizontal_distance(self,other):
        self_center = int(self.x1 + self.width()/2)
        other_center = int(other.x1 + other.width()/2)
        return abs(self_center-other_center)

    def vertical_distance(self,other):
        self_center = int(self.y1 + self.height()/2)
        other_center = int(other.y1 + other.height()/2)
        return abs(self_center-other_center)

    def __str__(self):
        s = "<ScreenObject x1={} y1={} x2={} y2={} text='{}' confidence={} />".format(
            self.x1, self.y1, self.x2, self.y2, self.text, self.confidence)
        return s

    # Returns the intersection area of this and the other object
    def intersection(self, other):
        max_x1 = max(self.x1, other.x1)
        min_x2 = min(self.x2, other.x2)

        x_diff = min_x2 - max_x1

        if x_diff < 0:
            return 0

        max_y1 = max(self.y1, other.y1)
        min_y2 = min(self.y2, other.y2)

        y_diff = min_y2 - max_y1

        if y_diff < 0:
            return 0

        return x_diff * y_diff

    def merge(self, other):
      if other.text != "":
        if self.x1 < other.x1:
          self.text = self.text + other.text
        else:
          self.text = other.text + self.text

      self.x1 = min(self.x1, other.x1)
      self.x2 = max(self.x2, other.x2)
      self.y1 = min(self.y1, other.y1)
      self.y2 = max(self.y2, other.y2)

      self.confidence = max(self.confidence, other.confidence)

    def __str__(self):
      return "ScreenObject {} ({} {}) ({} {})".format(self.text,self.x1,self.y1,self.x2,self.y2)


def detection(image, )
    """
    # Object Detection

    Object detection refers to the extraction of visible UI elements from the screenshot.
    We are using multiple methods and combining the results to accommodate for different types
    of UI elements and to increase the confidence level each extraction.
    """



    """## Edge Detection

    The most basic method we are using is edge detection.
    This is done by exploiting the differences in contrast between UI elements and the background.
    Our edge detection algorithm starts by converting the image to grayscale because we are mostly interested in
    contrast differences and the color information is unrelated in that context.
    Then a dilation step is applied to the images which causes very close together elements to blend into each other.
    This is done to detect singular elements which are composed of multiple near but separated components.
    Then we apply binary thresholding to the image which will transform it to a purely black and white image
    (all gray parts are converted to either black or white).
    We tried multiple algorithms for the binarization step and decided to use Otsu’s binarization.
    Otsu’s method does not require any parameter adjustment and is unsupervised (cite otsu).
    The resulting image is then fed to the contour analysis function of OpenCV which gives a sufficiently accurate detection
    of all the edges on the screen. Each edge in this case is considered a separate object.
    This method does have a high false positive rate and as a result the
    confidence level for objects detected with this method are considered low.

    """

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

    img_objs = image.copy()
    for obj in objs:
      x1,y1,x2,y2 = obj.get_xyxy()
      cv2.rectangle(img_objs, (x1,y1), (x2,y2), (0,255,0), 3)


    """## Text Detection OCR

    Edge detection can also be used to detect text.
    Due to the dilation step in the edge detection algorithm the different letters of paragraphs often blend together
    and make it possible to detect them as a single object.
    However, this is not very reliable since certain letters and fonts may not blend and cause paragraphs to be divided.
    It is also infeasible to distinguish between text objects and other objects.
    REMAUI uses Google’s Tesseract OCR to detect text to overcome these problems. (cite remaui).
    We followed a similar approach but instead used EasyOCR (cite easyocr).
    In our tests, it was more accurate than Tesseract and did not require
    installing anything on the user’s side unlike Tesseract. With EasyOCR we are able to detect text with high accuracy
    and also recognize the text which is also added to the output representation.
    """
    ocr_cache_file = image_filename + ".ocr.pickle"
    ocr_cache_file_path = os.path.join(data_dir, ocr_cache_file)

    objs2 = None

    if os.path.exists(ocr_cache_file_path):
        file = open(ocr_cache_file_path, "rb")
        objs2 = pickle.load(file)
        file.close()
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

        file = open(ocr_cache_file_path, "wb")
        pickle.dump(objs2, file)
        file.close()


    objs = objs + objs2

    """# Object Filtering

    This operation reduces the number of objects to ease the processing of the next operations.
    This is done by removing and combining objects according to some heuristics.
    Firstly, we remove any object too small to be noticeable or noteworthy.
    We defined the threshold of being too small as being less than 1% of the screen area.
    Then, any object contained in its entirety by another larger object is moved to be a child of the larger object.
    If these two objects were very similarly sized in terms of screen area, then the smaller object is removed altogether.
    We tuned these heuristics for use with the usually small screens of home appliances.
    However they are adjustable if the user has different requirements.

    """

    size = len(objs)

    remove_set = set()

    thresh = 0.8

    img_height, img_width, _ = image.shape
    img_area = img_height*img_width

    for i in range(size):
      obj1 = objs[i]

      if obj1.area() > img_area*0.5:
        remove_set.add(obj1)
        continue

      if obj1.width() < img_width*0.01:
        remove_set.add(obj1)
        continue

      if obj1.height() < img_height*0.01:
        remove_set.add(obj1)
        continue

      for j in range(i + 1, size):

          obj2 = objs[j]

          inter_area = obj1.intersection(obj2)

          if obj1.confidence < obj2.confidence:
              if inter_area > (obj1.area() * thresh):
                  remove_set.add(obj1)
          elif obj1.confidence > obj2.confidence:
              if inter_area > (obj2.area() * thresh):
                  remove_set.add(obj2)
          else:
              if inter_area > (obj2.area() * 0.6) and inter_area > (obj1.area() * 0.6):
                if obj1.area() < obj2.area():
                  remove_set.add(obj1)
                else:
                  remove_set.add(obj2)



    new_objs = []
    for obj in objs:
        if obj not in remove_set:
            new_objs.append(obj)

    print("Removed:", len(objs)-len(new_objs))

    img_filter = image.copy()
    for obj in new_objs:
      x1,y1,x2,y2 = obj.get_xyxy()
      cv2.rectangle(img_filter, (x1,y1), (x2,y2), (125,125,0), 2)

    objs = new_objs

    return objs


"""# Object Merging

Here we merge very close together text objects. And icons with nearby text objects are merged into those text objects

## Text Merge
"""

def horizontal_diff(obj1, obj2):
  x11,_,x12,_ = obj1.get_xyxy()
  x21,_,x22,_ = obj2.get_xyxy()

  val1 = abs(x12 - x21)
  val2 = abs(x22 - x11)

  return min(val1,val2)


cnt = 0
merge_indices = [-1 for i in range(len(objs))]
for i in range(len(objs)):

  obj1 = objs[i]
  if obj1.text == "":
    continue

  for j in range(i+1,len(objs)):
    obj2 = objs[j]

    if obj2.text == "":
      continue

    ver_diff = obj1.vertical_distance(obj2)
    hor_diff = horizontal_diff(obj1,obj2)

    if  ver_diff < img_height*0.01 and hor_diff < img_width*0.01:
      print(i,j)
      merge_index = max([merge_indices[i], merge_indices[j]])

      if merge_index == -1:
        merge_index = cnt
        cnt += 1

      merge_indices[i] = merge_index
      merge_indices[j] = merge_index


merge_dict = {i:[] for i in range(cnt)}
for i in range(len(merge_indices)):
  val = merge_indices[i]
  if val == -1:
    continue

  merge_dict[val].append(i)

remove_set = set()
for group in merge_dict.values():
  for i in range(1,len(group)):
    objs[group[0]].merge(objs[group[i]])
    remove_set.add(objs[group[i]])

new_objs = []
for obj in objs:
  if obj not in remove_set:
    new_objs.append(obj)

img_text_merge = image.copy()
for obj in new_objs:
  x1,y1,x2,y2 = obj.get_xyxy()
  cv2.rectangle(img_text_merge, (x1,y1), (x2,y2), (125,125,0), 3)


objs = new_objs

"""
## Icon - Text Merge

In this steps icons and text objects that are close together are merged into one

"""

remove_set = set()
for icon in objs:

  min_dist = 100000000
  min_text = None

  if icon.text != "" or abs(icon.width()-icon.height()) > img_width*0.05:
    continue

  for text in objs:
    if text.text == "" or text.text.isnumeric():
      continue

    dist = icon.vertical_distance(text)
    dist += icon.horizontal_distance(text)

    if dist < min_dist:
      min_dist = dist
      min_text = text

  if min_dist < img_width*0.15:
    print("Merging:", min_text.text)
    min_text.merge(icon)
    remove_set.add(icon)

new_objs = []
for obj in objs:
  if obj not in remove_set:
    new_objs.append(obj)

img_icon_merge = image.copy()
for obj in new_objs:
  x1,y1,x2,y2 = obj.get_xyxy()
  cv2.rectangle(img_icon_merge, (x1,y1), (x2,y2), (125,125,0), 3)

cv2.imwrite(os.path.join(image_dir, image_filename + ".filtering.jpg"), img_icon_merge)

objs = new_objs

"""# Clustering

##Compute padding between objects
"""

ver_dists = {obj: [] for obj in objs}
hor_dists = {obj: [] for obj in objs}
for obj1 in objs:
  for obj2 in objs:
    if obj1 != obj2:
      ver_dists[obj1].append(obj1.vertical_distance(obj2))
      hor_dists[obj1].append(obj1.horizontal_distance(obj2))
  ver_dists[obj1].sort()
  hor_dists[obj1].sort()

"""## Prepare Clustering Data"""

position_weight = 0.4
size_weight = 0.1
obj_type_weight = 0
padding_weight = 0.5

data = []
for obj in objs:
  point = []

  # Position of object
  center = obj.get_center()
  point += [center[0]*position_weight, center[1]*position_weight] # Indices 0,1 are position

  # Size of object
  point += [obj.area()*size_weight] # Index 2 is size

  # Whether it is a text object
  point += [int(obj.text != "")*obj_type_weight] # Index 3 is object type

  point += [x*padding_weight for x in ver_dists[obj][:2]] # Indices 4,5 are vertical padding
  point += [x*padding_weight for x in hor_dists[obj][:2]] # Indices 6,7 are horizontal padding

  data.append(point)

normalized_data = Normalizer().fit_transform(data)
print(normalized_data)

labels = None
method = "dbscan"
if method == "dbscan":
    db = cluster.DBSCAN(eps=0.2, min_samples=3).fit(normalized_data)
    labels = db.labels_
elif method == "meanshift":
    bandwidth = cluster.estimate_bandwidth(normalized_data, quantile=0.3, n_samples=10)
    ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(normalized_data)
    labels = ms.labels_
else:
    af = cluster.AffinityPropagation(random_state=0).fit(normalized_data)
    labels = af.labels_

# In RGB Format
colors = [
   [255,0,0], # Red
   [0,255,0], # Lime
   [0,0,255], # Blue
   [255,255,0], # Yellow
   [0,255,255], # Cyan
   [255,0,255], # Magenta
   [255,128,0], # Orange
   [127,0,255], # Purple
   [255,153,255], # Pink
]

# OpenCV uses BGR instead of RGB for some reason
# So here we reverse all elements of the array
colors = [tuple(reversed(color)) for color in colors]


"""# Post-Processing"""

def compute_menu(cls):
  inf = 1000000
  menu = [inf,inf,0,0]
  for obj in cls:
    menu[0] = min(obj.x1, menu[0])
    menu[1] = min(obj.y1, menu[1])
    menu[2] = max(obj.x2, menu[2])
    menu[3] = max(obj.y2, menu[3])
  return menu


clusters = {label:set() for label in labels}
for i,obj in enumerate(objs):
  label = labels[i]
  clusters[label].add(obj)

print(clusters)

menus = [compute_menu(cls) for cls in clusters.values()]
print(menus)

img_menus = image.copy()
for i,menu in enumerate(menus):
  cv2.rectangle(img_menus, (menu[0],menu[1]), (menu[2], menu[3]), colors[i % len(colors)], 2)
cv2.imwrite(os.path.join(image_dir, image_filename + ".clustering.jpg"), img_menus)


def intersects(b1, b2):
  hor_diff = (b1[3] < b2[1]) or (b2[3] < b1[1])
  ver_diff = (b1[2] < b2[0]) or (b2[2] < b2[0])
  return not (hor_diff or ver_diff)

def solve_intersection(cls1, cls2):
  if cls1 == cls2:
    return

  menu1 = compute_menu(cls1)
  menu2 = compute_menu(cls2)

  if intersects(menu1, menu2):
    intersection = [0,0,10000000,100000000]

    intersection[0] = max(menu1[0], menu2[0])
    intersection[1] = max(menu1[1], menu2[1])
    intersection[2] = min(menu1[2], menu2[2])
    intersection[3] = min(menu1[3], menu2[3])

    inter_objs = [obj for obj in set.union(cls1,cls2) if intersects(obj.get_xyxy(), intersection)]

    for i in range(1,3):

      if len(inter_objs) < i:
          break

      for _ in range(1000):
        selected_objs = set(random.sample(inter_objs, i))

        # Swap Selected Objects
        for obj in selected_objs:
          if obj in cls1:
            cls1.remove(obj)
            cls2.add(obj)
          elif obj in cls2:
            cls2.remove(obj)
            cls1.add(obj)

        # Check if the swap solved the intersection
        if not intersects(compute_menu(cls1), compute_menu(cls2)):
          print("Solved intersection with {} swaps".format(i))
          return

        # Swap Back
        for obj in selected_objs:
          if obj in cls1:
            cls1.remove(obj)
            cls2.add(obj)
          elif obj in cls2:
            cls2.remove(obj)
            cls1.add(obj)



for _ in range(3):
  for cls1 in clusters.values():
    for cls2 in clusters.values():
      solve_intersection(cls1,cls2)

menus2 = [compute_menu(cls) for cls in clusters.values()]
print(menus2)

img_menus2 = image.copy()
for i,menu in enumerate(menus2):
  if menu != [1000000, 1000000, 0, 0]:
    cv2.rectangle(img_menus2, (menu[0],menu[1]), (menu[2], menu[3]), colors[i % len(colors)], 2)

cv2.imwrite(os.path.join(image_dir, image_filename + ".final.jpg"), img_menus)

root_elem = ET.Element('root')
for cls in clusters.values():
    cls_elem = ET.SubElement(root_elem, 'cluster')

    for obj in cls:
        x1,y1,x2,y2 = obj.get_xyxy()
        _,_,w,h = obj.get_xywh()
        obj_elem = ET.SubElement(cls_elem, 'object')
        obj_elem.set('x1',x1)
        obj_elem.set('x2',x2)
        obj_elem.set('y1',y1)
        obj_elem.set('y2',y2)
        obj_elem.set('w',w)
        obj_elem.set('h',h)
        obj_elem.set('text', obj.text)

xml_str = ET.tostring(root_elem)

xml_file = open(os.path.join(data_dir, image_filename + ".xml"), "w+")
xml_file.write(xml_str)
xml_file.close()
