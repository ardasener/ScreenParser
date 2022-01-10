import cv2
from screen_object import ScreenObject
import pickle
import sys
from sklearn import cluster
from sklearn.preprocessing import Normalizer
import os
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


def prepare_data(objs):

    ver_dists = {obj: [] for obj in objs}
    hor_dists = {obj: [] for obj in objs}
    for obj1 in objs:
      for obj2 in objs:
        if obj1 != obj2:
          ver_dists[obj1].append(obj1.vertical_distance(obj2))
          hor_dists[obj1].append(obj1.horizontal_distance(obj2))


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

      point += [min(ver_dists[obj])]
      point += [min(hor_dists[obj])]

      data.append(point)

    normalized_data = Normalizer().fit_transform(data)
    return normalized_data

def dbscan(data):
    db = cluster.DBSCAN(eps=0.2, min_samples=3).fit(data)
    db_labels = db.labels_
    return db_labels

def meanshift(data):
    bandwidth = cluster.estimate_bandwidth(normalized_data, quantile=0.3, n_samples=10)
    ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(data)
    ms_labels = ms.labels_

def affinity_prop(data):
    af = cluster.AffinityPropagation(random_state=0).fit(data)
    af_labels = af.labels_


def main(all_objs, image_files ,image_dir):

    all_clusters = []
    for image_id,objs in enumerate(all_objs):

        data = prepare_data(objs)
        labels = dbscan(data)

        clusters = {label:set() for label in labels}
        for i,obj in enumerate(objs):
          label = labels[i]
          clusters[label].add(obj)

        menus = [compute_menu(cls) for cls in clusters.values()]


        image_file = image_files[image_id]
        image = cv2.imread(image_file)
        filename = os.path.basename(image_file).split(".")[0]
        for i,menu in enumerate(menus):
            cv2.rectangle(image, (menu[0], menu[1]), (menu[2], menu[3]), colors.get_color(i),2)
        cv2.imwrite(os.path.join(image_dir, filename + ".clustering.jpg"),image)

        all_clusters.append(clusters)

    return all_clusters