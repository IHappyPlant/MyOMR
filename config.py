from mrcnn.config import Config


class MyConfig(Config):

    def __init__(self):
        super().__init__()

    NAME = "1065_cfg"
    NUM_CLASSES = 1 + 1 + 1 + 1
    STEPS_PER_EPOCH = 122
    GPU_COUNT = 1
    IMAGES_PER_GPU = 10


# define the prediction configuration
class PredictionConfig(Config):
    # define the name of the configuration
    def __init__(self):
        super().__init__()

    NAME = "1065_cfg"
    # number of classes (background + others)
    NUM_CLASSES = 1 + 1 + 1 + 1
    # simplify GPU config
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
