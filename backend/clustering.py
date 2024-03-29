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


def prepare_data(objs, image, config):
    img_height, img_width, _ = image.shape
    img_area = img_height*img_width

    ver_dists = {obj: [] for obj in objs}
    hor_dists = {obj: [] for obj in objs}
    for obj1 in objs:
      for obj2 in objs:
        if obj1 != obj2:
          ver_dist = obj1.vertical_distance(obj2)
          hor_dist = obj1.horizontal_distance(obj2)
          if ver_dist > img_height*0.01:
            ver_dists[obj1].append(ver_dist)
          if hor_dist > img_width*0.01:
            hor_dists[obj1].append(hor_dist)


    position_weight = config["position_weight"]
    size_weight = config["size_weight"]
    obj_type_weight = config["type_weight"]
    padding_weight = config["padding_weight"]

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

      point += [min(ver_dists[obj])*padding_weight if len(ver_dists[obj]) > 0 else 0]
      point += [min(hor_dists[obj])*padding_weight if len(hor_dists[obj]) > 0 else 0]

      data.append(point)

    normalized_data = Normalizer().fit_transform(data)
    return normalized_data

def dbscan(data, config):
    db = cluster.DBSCAN(eps=config["dbscan_eps"], min_samples=config["dbscan_min_samples"]).fit(data)
    db_labels = db.labels_
    return db_labels

def meanshift(data, config):
    bandwidth = cluster.estimate_bandwidth(data, quantile=config["ms_quantile"], n_samples=config["ms_n_samples"])
    ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(data)
    ms_labels = ms.labels_
    return ms_labels

def affinity_prop(data):
    af = cluster.AffinityPropagation(random_state=0).fit(data)
    af_labels = af.labels_
    return af_labels


def main(all_objs, image_files ,image_dir, config, run_id):

    print(config)

    all_clusters = []
    for image_id,objs in enumerate(all_objs):
        image_file = image_files[image_id]
        image = cv2.imread(image_file)

        data = prepare_data(objs, image, config)

        labels = None
        method = config["clustering_alg"]
        print("Clustering with method: {} ...".format(method))
        if method == "dbscan":
            labels = dbscan(data, config)
        elif method == "meanshift":
            labels = meanshift(data, config)
        else:
            labels = affinity_prop(data)

        clusters = {label:set() for label in labels}
        for i,obj in enumerate(objs):
          label = labels[i]
          clusters[label].add(obj)

        menus = [compute_menu(cls) for cls in clusters.values()]



        filename = os.path.basename(image_file).split(".")[0]
        for i,menu in enumerate(menus):
            cv2.rectangle(image, (menu[0], menu[1]), (menu[2], menu[3]), colors.get_color(i),3)
        cv2.imwrite(os.path.join(image_dir, filename + "_" + str(run_id) + ".clustering.jpg"),image)

        all_clusters.append(clusters)

    return all_clusters