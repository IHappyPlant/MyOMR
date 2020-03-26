import cv2
import numpy as np
import skimage.io
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mrcnn.model import MaskRCNN
from mrcnn.model import mold_image

import scoring
from omr_configs import TrainConfig, PredictConfig
from dataset import MyDataset
from img_preprocess import binarize_img


def image_info_from_annot(dataset_image_info, class_names):
    annot = dataset_image_info['annotation']
    classes = MyDataset.extract_classes(annot)
    boxes = np.array(MyDataset.extract_boxes(annot)[0])
    class_indexes = [class_names.index(classes[i]) for i in range(len(classes))]
    return {
        'boxes': boxes,
        'classes': class_indexes
    }


def get_image_info_by_id(dataset_, image_id):
    for image_info in dataset_.image_info:
        if int(image_info['id']) == image_id:
            return image_info


def predict_and_display(image, sample, model, real_classes=None):
    pyplot.imshow(image)
    ax = pyplot.gca()
    yhat = model.detect(sample, verbose=0)[0]
    colors = ['white', 'red', 'green', 'blue']
    i = 0
    print(yhat['class_ids'])
    for box in yhat['rois']:
        # get coordinates
        y1, x1, y2, x2 = box
        # calculate width and height of the box
        width, height = x2 - x1, y2 - y1
        # create the shape
        rect = Rectangle((x1, y1), width, height, fill=False, color=colors[
            yhat['class_ids'][i]])
        i += 1
        # draw the box
        ax.add_patch(rect)
    # show the figure
    if real_classes:
        matrix = scoring.build_confusion_matrix([yhat], [real_classes], 4)
        for row in matrix:
            print(row)
        scores = scoring.get_all_scores(matrix, [0, 1, 2, 3])
        print(scores)
    pyplot.show()
    # print(scoring.build_confusion_matrix([yhat], [real_classes], 3))


def test(dataset_, model, cfg):
    predicts = []
    groundtruths = []
    image_infos = sorted(dataset_.image_info, key=lambda x: int(x['id']))
    i = 0
    for image_info in image_infos:
        image_info['id'] = str(i)
        i += 1
    dataset_.image_info = image_infos
    for i in dataset_.image_ids:
        img = dataset_.load_image(i)
        img_info = get_image_info_by_id(dataset_, i)
        if not img_info:
            continue
        groundturh_img = image_info_from_annot(img_info, dataset_.class_names)
        scaled_image = mold_image(img, cfg)
        sample = np.expand_dims(scaled_image, 0)
        yhat = model.detect(sample, verbose=0)[0]
        predicts.append(yhat)
        groundtruths.append(groundturh_img)
    matrix = scoring.build_confusion_matrix(predicts, groundtruths, 4)
    scores = scoring.get_all_scores(matrix, [0, 1, 2, 3])
    for row in matrix:
        print(row)
    print(scores)


# prepare train set
train_set = MyDataset()
train_set.load_dataset('1065dataset', is_train=True)
train_set.prepare()
print('Train: %d' % len(train_set.image_ids))
# prepare test/val set
test_set = MyDataset()
test_set.load_dataset('1065dataset', is_train=False)
test_set.prepare()
print('Test: %d' % len(test_set.image_ids))

# cfg = TrainConfig()
# model = MaskRCNN(mode='training', model_dir='./', config=cfg)
# model.load_weights('mask_rcnn_coco.h5', by_name=True, exclude=[
#     'conv1', "mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"])
# model.train(train_set, test_set, learning_rate=cfg.LEARNING_RATE, epochs=50,
#             layers=r"conv1|(mrcnn\_.*)|(rpn\_.*)|(fpn\_.*)")

cfg = PredictConfig()
model = MaskRCNN('inference', model_dir='./', config=cfg)
model.load_weights('mask_rcnn_1065_cfg_0010.h5', by_name=True)
#
path_to_sample = '1065dataset/1.jpg'
# binarize_img(path_to_sample, '1065dataset/0000.jpg', 164, 255)
# path_to_annot = '1065dataset/annots/0000.xml'
# img_info = get_image_info_by_id(train_set, 0)
# groundturh_img = image_info_from_annot(img_info, train_set.class_names)
sample = skimage.io.imread(path_to_sample, as_gray=True)
sample1 = cv2.imread(path_to_sample, 2)
image = np.copy(sample)
sample = np.expand_dims(sample, 2)
# sample = cv2.imread(path_to_sample)
# image = np.copy(sample)
scaled_image = mold_image(sample, cfg)
sample = np.expand_dims(scaled_image, 0)
predict_and_display(image, sample, model)
# test(train_set, model, cfg)


# from PIL import Image
# desired_size = 512
# im = Image.open(path_to_sample)
# old_size = im.size
# ratio = float(desired_size) / max(old_size)
# new_size = tuple([int(x * ratio) for x in old_size])
# im = im.resize(new_size, Image.ANTIALIAS)
# im.save('1065dataset/0000.jpg')
