import graphlib
import matplotlib.pyplot as plt
from mrcnn.model import MaskRCNN
from mrcnn.config import Config
import tensorflow as tf

class BrailleConfig(Config):
    '''
    Defines a configuration for the model
    '''

    #Set the configuration a recognizable name
    NAME = "AIBL_cfg"

    #Set number of classes - background + num of braille cells being trained
    NUM_CLASSES = 1 + 26

    #number of training steps per epoch
    STEPS_PER_EPOCH = 131

    GPU_COUNT = 1
    IMAGES_PER_GPU = 1



config = BrailleConfig()


#Define model
model = MaskRCNN(mode="inference", model_dir="./", config=config)

#Specify keras file with weights
model_path="../mask_rcnn_aibl_cfg_0005.h5"

#Load weights   
model.load_weights(model_path, by_name=True)

model.keras_model._make_predict_function()


def predict(img_path):
    img = plt.imread(img_path)

    return model.detect([img], verbose=0)





