import os
from xml.etree import ElementTree

import numpy as np
from mrcnn.utils import Dataset


class MyDataset(Dataset):

    def __init__(self):
        super().__init__()

    def load_dataset(self, dataset_dir, is_train=True):
        self.add_class('dataset', 1, 'unfilled checkbox')
        self.add_class('dataset', 2, 'filled checkbox')
        self.add_class('dataset', 3, 'checkmark')
        images_dir = dataset_dir + '/images/'
        annotations_dir = dataset_dir + '/annots/'
        files = os.listdir(images_dir)
        cnt = 0
        for filename in files:
            image_id = filename[:-4]

            # if image_id in ['00090']:
            #     continue

            if is_train and cnt >= int(len(files) * 0.8):
                cnt += 1
                continue

            if not is_train and cnt < int(len(files) * 0.8):
                cnt += 1
                continue

            img_path = images_dir + filename
            ann_path = annotations_dir + str(image_id) + '.xml'
            self.add_image('dataset', image_id=image_id, path=img_path,
                           annotation=ann_path)
            cnt += 1

    def load_mask(self, image_id):
        info = self.image_info[image_id]
        path = info['annotation']
        names = self.extract_classes(path)
        boxes, w, h = self.extract_boxes(path)
        masks = np.zeros([h, w, len(boxes)], dtype='uint8')
        class_ids = []
        for i in range(len(boxes)):
            box = boxes[i]
            row_s, row_e = box[1], box[3]
            col_s, col_e = box[0], box[2]
            masks[row_s:row_e, col_s:col_e, i] = 1
            class_ids.append(self.class_names.index(names[i]))
        return masks, np.asarray(class_ids, dtype='int32')

    @staticmethod
    def extract_boxes(file_name):
        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        boxes = []
        for box in root.findall('.//bndbox'):
            xmin = int(box.find('xmin').text)
            ymin = int(box.find('ymin').text)
            xmax = int(box.find('xmax').text)
            ymax = int(box.find('ymax').text)
            boxes.append([xmin, ymin, xmax, ymax])
        width = int(root.find('.//size/width').text)
        height = int(root.find('.//size/height').text)
        return boxes, width, height

    @staticmethod
    def extract_classes(file_name):
        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        names = []
        for name in root.findall('.//name'):
            names.append(name.text)
        return names

    def image_reference(self, image_id):
        info = self.image_info[image_id]
        return info['path']
