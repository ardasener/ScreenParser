import cv2
from screen_object import ScreenObject
import pickle
import sys
import xml.etree.ElementTree as ET
import os
import random
import colors

def compute_menu(cls):
  inf = 1000000
  menu = [inf,inf,0,0]
  for obj in cls:
    menu[0] = min(obj.x1, menu[0])
    menu[1] = min(obj.y1, menu[1])
    menu[2] = max(obj.x2, menu[2])
    menu[3] = max(obj.y2, menu[3])
  return menu


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


def clusters_to_xml(clusters, filename):
    root_elem = ET.Element('root')
    for cls in clusters.values():
        cls_elem = ET.SubElement(root_elem, 'cluster')

        for obj in cls:
            x1,y1,x2,y2 = obj.get_xyxy()
            _,_,w,h = obj.get_xywh()
            obj_elem = ET.SubElement(cls_elem, 'object')
            obj_elem.set('x1',str(x1))
            obj_elem.set('x2',str(x2))
            obj_elem.set('y1',str(y1))
            obj_elem.set('y2',str(y2))
            obj_elem.set('w',str(w))
            obj_elem.set('h',str(h))
            obj_elem.set('text', obj.text)

    tree = ET.ElementTree(root_elem)
    tree.write(filename)


def main(all_clusters, image_files, data_dir, image_dir):
    for image_id,clusters in enumerate(all_clusters):

        for _ in range(3):
          for cls1 in clusters.values():
            for cls2 in clusters.values():
              solve_intersection(cls1,cls2)

        image_file = image_files[image_id]
        filename = os.path.basename(image_file).split(".")[0]
        image = cv2.imread(image_file)

        menus = [compute_menu(cls) for cls in clusters.values()]

        for i,menu in enumerate(menus):
            cv2.rectangle(image, (menu[0], menu[1]), (menu[2], menu[3]), colors.get_color(i),2)
        cv2.imwrite(os.path.join(image_dir, filename + ".final.jpg"),image)

        clusters_to_xml(clusters, os.path.join(data_dir, filename + ".xml"))
