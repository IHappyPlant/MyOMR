import os


def preprocess(images_dir, annots_dir):
    imgs = sorted([file.split('.')[0] for file in os.listdir(images_dir)],
                  key=lambda x: int(x))
    annots = sorted([file.split('.')[0] for file in os.listdir(annots_dir)],
                    key=lambda x: int(x))
