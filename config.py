from mrcnn.config import Config


class TrainConfig(Config):

    def __init__(self):
        super().__init__()

    NAME = "1065_cfg"
    NUM_CLASSES = 4
    STEPS_PER_EPOCH = 1000
    GPU_COUNT = 1
    IMAGES_PER_GPU = 2
    MEAN_PIXEL = 0
    VALIDATION_STEPS = 200
    IMAGE_RESIZE_MODE = 'square'
    IMAGE_MIN_DIM = 395
    IMAGE_MAX_DIM = 512
    IMAGE_CHANNEL_COUNT = 1
    # RPN_NMS_THRESHOLD = 0.9
    # RPN_TRAIN_ANCHORS_PER_IMAGE = 512


class PredictConfig(Config):
    def __init__(self):
        super().__init__()

    NAME = "1065_cfg"
    # number of classes (background + others)
    NUM_CLASSES = 4
    GPU_COUNT = 1
    IMAGES_PER_GPU = 2
    MEAN_PIXEL = 0
    IMAGE_RESIZE_MODE = 'square'
    IMAGE_MIN_DIM = 395
    IMAGE_MAX_DIM = 512
    IMAGE_CHANNEL_COUNT = 1
