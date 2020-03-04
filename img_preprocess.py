import os
from xml.etree import ElementTree
from PIL import Image, ImageOps


def preprocess(images_dir, annots_dir):
    imgs = [file for file in os.listdir(images_dir) if file.endswith('.jpg')]
    imgs = list(sorted([file.split('.')[0] for file in imgs],
                       key=lambda x: int(x)))
    annots = [file for file in os.listdir(annots_dir) if file.endswith('.xml')]
    annots = list(sorted([file.split('.')[0] for file in annots],
                         key=lambda x: int(x)))
    for i in range(len(imgs)):
        im_pth = os.path.join(images_dir, imgs[i] + '.jpg')
        annot_pth = os.path.join(annots_dir, annots[i] + '.xml')
        desired_size = 512
        im = Image.open(im_pth)
        old_size = im.size
        ratio = float(desired_size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        im = im.resize(new_size, Image.ANTIALIAS)
        im.save(images_dir + '/resized/' + str(imgs[i]) + '.jpg')

        update_xml(annot_pth, ratio, annots_dir + '/resized/' + annots[i] +
                   '.xml')


def update_xml(path_to_xml, ratio, path_to_output):
    model = ElementTree.parse(path_to_xml)
    root = model.getroot()
    for size in root.iter('size'):
        txt = size.find('width').text
        size.find('width').text = str(int(int(txt) * ratio))
        txt = size.find('height').text
        size.find('height').text = str(int(int(txt) * ratio))

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


# desired_size = 512
# im_pth = '1065dataset/images/0000.jpg'
#
# im = Image.open(im_pth)
# old_size = im.size
# print(old_size)
# ratio = float(desired_size) / max(old_size)
# print(ratio)
# new_size = tuple([int(x*ratio) for x in old_size])
#
#
# im = im.resize(new_size, Image.ANTIALIAS)
# print(im.size)
# im.save('test.jpg')
# new_im = Image.new('RGB', (desired_size, desired_size))
# new_im.paste(im, ((desired_size-new_size[0])//2, (desired_size-new_size[1])//2))
# new_im.show()

if __name__ == '__main__':
    preprocess('1065dataset/images', '1065dataset/annots')