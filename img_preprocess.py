import os
from xml.etree import ElementTree
from PIL import Image, ImageOps


def preprocess(images_dir, annots_dir):
    imgs = sorted([file.split('.')[0] for file in os.listdir(images_dir)],
                  key=lambda x: int(x))
    annots = sorted([file.split('.')[0] for file in os.listdir(annots_dir)],
                    key=lambda x: int(x))
    for i in range(len(imgs)):
        im_pth = os.path.join(images_dir, imgs[i])
        annot_pth = os.path.join(annots_dir, annots[i])
        desired_size = 512
        pass


def update_xml(path_to_xml, ratio):
    model = ElementTree.parse(path_to_xml)
    root = model.getroot()
    txt = ''
    for box in root.iter('bndbox'):
        txt = box.find('xmin').text
        box.find('xmin').text = str(int(int(txt) * ratio))
        txt = box.find('ymin').text
        box.find('ymin').text = str(int(int(txt) * ratio))
        txt = box.find('xmax').text
        box.find('xmax').text = str(int(int(txt) * ratio))
        txt = box.find('ymax').text
        box.find('ymax').text = str(int(int(txt) * ratio))

    pass
desired_size = 512
im_pth = '1065dataset/images/0000.jpg'

im = Image.open(im_pth)
old_size = im.size
print(old_size)
ratio = float(desired_size) / max(old_size)
print(ratio)
new_size = tuple([int(x*ratio) for x in old_size])


im = im.resize(new_size, Image.ANTIALIAS)
print(im.size)
im.save('test.jpg')
new_im = Image.new('RGB', (desired_size, desired_size))
new_im.paste(im, ((desired_size-new_size[0])//2, (desired_size-new_size[1])//2))
new_im.show()