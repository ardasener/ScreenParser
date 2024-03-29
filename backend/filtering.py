import cv2
from screen_object import ScreenObject
import pickle
import sys
import os

def filter(objs, image, config):

    size = len(objs)

    remove_set = set()

    img_height, img_width, _ = image.shape
    img_area = img_height*img_width

    for i in range(size):
      obj1 = objs[i]

      if obj1.area() > img_area * config["large_obj_threshold"]:
        remove_set.add(obj1)
        continue

      if obj1.width() < img_width * config["small_obj_threshold"]:
        remove_set.add(obj1)
        continue

      if obj1.height() < img_height * config["small_obj_threshold"]:
        remove_set.add(obj1)
        continue

      thresh = config["intersection_threshold"]

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
              if inter_area > (obj2.area() * thresh) and inter_area > (obj1.area() * thresh):
                if obj1.area() < obj2.area():
                  remove_set.add(obj1)
                else:
                  remove_set.add(obj2)



    new_objs = []
    for obj in objs:
        if obj not in remove_set:
            new_objs.append(obj)

    print("Removed:", len(objs)-len(new_objs))


    return new_objs


def text_merge(objs, image, config):

    img_height, img_width, _ = image.shape
    img_area = img_height*img_width


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

        thresh = config["text_merge_threshold"]
        if  ver_diff < img_height*thresh and hor_diff < img_width*thresh:
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

    return new_objs

def icon_text_merge(objs, image, config):
    img_height, img_width, _ = image.shape
    img_area = img_height*img_width

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

      if min_dist < img_width * config["icon_text_merge_threshold"]:
        print("Merging:", min_text.text)
        min_text.merge(icon)
        remove_set.add(icon)

    new_objs = []
    for obj in objs:
      if obj not in remove_set:
        new_objs.append(obj)


    return new_objs


def main(all_objs, image_files, image_dir, config, run_id):

    print(config)

    new_all_objs = []
    for image_id,objs in enumerate(all_objs):
        image_file = image_files[image_id]
        image = cv2.imread(image_file)

        print("Applying filtering...")
        objs = filter(objs, image, config)
        print("Applying text/text merge...")
        objs = text_merge(objs, image, config)
        print("Applying text/icon merge...")
        objs = icon_text_merge(objs, image, config)


        filename = os.path.basename(image_file).split(".")[0]
        for obj in objs:
          x1,y1,x2,y2 = obj.get_xyxy()
          cv2.rectangle(image, (x1,y1), (x2,y2), (125,125,0), 3)

        cv2.imwrite(os.path.join(image_dir, filename + "_" + str(run_id) + ".filtering.jpg"),image)
        new_all_objs.append(objs)

    return new_all_objs

