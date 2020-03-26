import os
from xml.etree import ElementTree

import cv2
from PIL import Image


def preprocess(images_dir, annots_dir, desired_size=512):
    imgs = [file for file in os.listdir(images_dir) if file.endswith('.jpg')]
    imgs = list(sorted([file.split('.')[0] for file in imgs],
                       key=lambda x: int(x)))
    annots = [file for file in os.listdir(annots_dir) if file.endswith('.xml')]
    annots = list(sorted([file.split('.')[0] for file in annots],
                         key=lambda x: int(x)))
    for i in range(len(imgs)):
        im_pth = os.path.join(images_dir, imgs[i] + '.jpg')
        annot_pth = os.path.join(annots_dir, annots[i] + '.xml')
        im = Image.open(im_pth)
        old_size = im.size
        ratio = float(desired_size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        im = im.resize(new_size, Image.ANTIALIAS)
        im.save(images_dir + '/resized/' + str(imgs[i]) + '.jpg')

        update_xml(annot_pth, ratio, annots_dir + '/resized/' + annots[i] +
                   '.xml')


def resize_image(im_pth, size=512):
    im = Image.open(im_pth)
    old_size = im.size
    ratio = float(size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    im = im.resize(new_size, Image.ANTIALIAS)
    img_name = im_pth.split('.')[0]
    im.save(img_name + '_resized.jpg')


def update_xml(path_to_xml, ratio, path_to_output):
    model = ElementTree.parse(path_to_xml)
    root = model.getroot()
    for size in root.iter('size'):
        txt = size.find('width').text
        size.find('width').text = str(int(int(txt) * ratio))
        txt = size.find('height').text
        size.find('height').text = str(int(int(txt) * ratio))
        size.find('depth').text = str(1)

    for box in root.iter('bndbox'):
        txt = box.find('xmin').text
        box.find('xmin').text = str(int(int(txt) * ratio))
        txt = box.find('ymin').text
        box.find('ymin').text = str(int(int(txt) * ratio))
        txt = box.find('xmax').text
        box.find('xmax').text = str(int(int(txt) * ratio))
        txt = box.find('ymax').text
        box.find('ymax').text = str(int(int(txt) * ratio))

    tree = ElementTree.ElementTree(root)
    tree.write(path_to_output, encoding='utf-8')


def binarize_img(path_to_img, path_to_output='binarized.jpg', threshold=128,
                 max_val=255):
    im = cv2.imread(path_to_img, 2)
    ret, bw_img = cv2.threshold(im, threshold, max_val, cv2.THRESH_BINARY)
    cv2.imwrite(path_to_output, bw_img)


# if __name__ == '__main__':
#     preprocess('1065dataset/changed', '1065dataset/annots_new')
#
# images_dir = '1065dataset/changed'
# imgs = [file for file in os.listdir(images_dir)
#         if file.endswith('.jpg')]
# imgs = list(sorted([file.split('.')[0] for file in imgs],
#                    key=lambda x: int(x)))
# for i in range(len(imgs)):
#     im_pth = os.path.join(images_dir, imgs[i] + '.jpg')
#     binarize_img(im_pth, '/home/alex/Documents/PyCharmProjects/MyOMR/'
#                          '1065dataset/changed/binarized/' + str(imgs[i]) +
#                  '.jpg', 164, 255)
