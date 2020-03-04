import imgaug
import numpy as np
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mrcnn.model import MaskRCNN
from mrcnn.model import load_image_gt
from mrcnn.model import mold_image
from mrcnn.utils import compute_ap

import scoring
from config import MyConfig
from dataset import MyDataset


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


# calculate the mAP for a model on a given dataset
def evaluate_model(dataset, model, cfg):
    APs = list()
    for image_id in dataset.image_ids:
        # load image, bounding boxes and masks for the image id
        image, image_meta, gt_class_id, gt_bbox, gt_mask = load_image_gt(
            dataset, cfg, image_id, use_mini_mask=False)
        # convert pixel values (e.g. center)
        scaled_image = mold_image(image, cfg)
        # convert image into one sample
        sample = np.expand_dims(scaled_image, 0)
        # make prediction
        yhat = model.detect(sample, verbose=0)
        # extract results for first sample
        r = yhat[0]
        # calculate statistics, including AP
        AP, _, _, _ = compute_ap(gt_bbox, gt_class_id, gt_mask, r["rois"],
                                 r["class_ids"], r["scores"], r['masks'])
        # store
        APs.append(AP)
    # calculate the mean AP across all images
    mAP = np.mean(APs)
    return mAP


# plot a number of photos with ground truth and predictions
def plot_actual_vs_predicted(dataset, model, cfg, n_images=4):
    # load image and mask
    for i in range(n_images):
        # load the image and mask
        image = dataset.load_image(i)
        mask, _ = dataset.load_mask(i)
        # convert pixel values (e.g. center)
        scaled_image = mold_image(image, cfg)
        # convert image into one sample
        sample = np.expand_dims(scaled_image, 0)
        # make prediction
        yhat = model.detect(sample, verbose=0)[0]
        # define subplot
        pyplot.subplot(n_images, 2, i * 2 + 1)
        # plot raw pixel data
        pyplot.imshow(image)
        pyplot.title('Actual')
        # plot masks
        for j in range(mask.shape[2]):
            pyplot.imshow(mask[:, :, j], cmap='gray', alpha=0.3)
        # get the context for drawing boxes
        pyplot.subplot(n_images, 2, i * 2 + 2)
        # plot raw pixel data
        pyplot.imshow(image)
        pyplot.title('Predicted')
        ax = pyplot.gca()
        # plot each box
        for box in yhat['rois']:
            # get coordinates
            y1, x1, y2, x2 = box
            # calculate width and height of the box
            width, height = x2 - x1, y2 - y1
            # create the shape
            rect = Rectangle((x1, y1), width, height, fill=False, color='red')
            # draw the box
            ax.add_patch(rect)
    # show the figure
    pyplot.show()


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


def load_model(mode, path_to_weights, config):
    model = MaskRCNN(mode=mode, model_dir='./', config=cfg)
    model.load_weights(path_to_weights, by_name=True)
    return model


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

cfg = MyConfig()
aug = imgaug.augmenters.Sometimes(0.5, [
    imgaug.augmenters.Fliplr(0.5),
    imgaug.augmenters.GaussianBlur(sigma=(0.0, 5.0))
])
model = MaskRCNN(mode='training', model_dir='./', config=cfg)
# load model weights
model.load_weights('mask_rcnn_coco.h5', by_name=True, exclude=[
    "mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"])
model.train(train_set, test_set, learning_rate=cfg.LEARNING_RATE, epochs=10,
            layers='heads', augmentation=aug)

# cfg = PredictionConfig()
# model = load_model('inference', 'mask_rcnn_1065_cfg_0004.h5', cfg)
#
# path_to_sample = '1065dataset/images/0000.jpg'
# path_to_annot = '1065dataset/annots/0000.xml'
# img_info = get_image_info_by_id(train_set, 0)
# groundturh_img = image_info_from_annot(img_info, train_set.class_names)
# sample = cv2.imread(path_to_sample)
# image = np.copy(sample)
# scaled_image = mold_image(sample, cfg)
# sample = np.expand_dims(scaled_image, 0)
# predict_and_display(image, sample, model, groundturh_img)
# # plot predictions for train dataset
# plot_actual_vs_predicted(train_set, model, cfg)
# # plot predictions for test dataset
# plot_actual_vs_predicted(test_set, model, cfg)

# path_to_sample = '1065dataset/0000.jpg'
# sample = cv2.imread(path_to_sample)
# image = np.copy(sample)
# scaled_image = mold_image(sample, cfg)
# sample = np.expand_dims(scaled_image, 0)
# # print(model.detect(sample, verbose=0)[0])
# predict_and_display(image, sample, model)
# test(train_set, model, cfg)
