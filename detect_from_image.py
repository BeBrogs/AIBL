
import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt

from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
import train_mask_rcnn

#Define root dir of project
ROOT_DIR = os.path.abspath("../")


#Directory of images
IMAGE_DIR = os.path.join(ROOT_DIR, "mask_rcnn", "BRAILLE", "numbered_images")


config = train_mask_rcnn.BrailleConfig()
config.display()




model = MaskRCNN(mode="inference", model_dir="./", config=config)

model_path = "mask_rcnn_aibl_cfg_0005.h5"

model.load_weights(model_path, by_name=True)


braille_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
class_names = ["BG"]
class_names = class_names + [i for i in braille_letters]

#Load random image from images folder
file_names = next(os.walk(IMAGE_DIR))[2]

image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))



results = model.detect([image], verbose=1)

r=results[0]

visualize.display_instances(image, r['rois'], r["masks"], r["class_ids"], class_names, r["scores"])
