from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from numpy import expand_dims
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
from mrcnn.model import mold_image
from mrcnn.utils import Dataset
import train_mask_rcnn 


# plot a number of photos with ground truth and predictions
def plot_actual_vs_predicted(dataset, model, cfg, n_images=15):
	# load image and mask
    for i in range(n_images):
		# load the image and mask
        image = dataset.load_image(i)
		mask, _ = dataset.load_mask(i)
		# convert pixel values (e.g. center)
		scaled_image = mold_image(image, cfg)
		# convert image into one sample
		sample = expand_dims(scaled_image, 0)
		# make prediction
		yhat = model.detect(sample, verbose=0)[0]
		# define subplot
		pyplot.subplot(10, 2, i*2+1)
		# plot raw pixel data
		pyplot.imshow(image)
		pyplot.title('Actual')
		# plot masks
		for j in range(mask.shape[2]):
			pyplot.imshow(mask[:, :, j], cmap='gray', alpha=0.05)
		# get the context for drawing boxes
		pyplot.subplot(n_images, 2, i*2+2)
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

if __name__ == "__main__":
    training_data = train_mask_rcnn.BrailleDataSet()
    training_data.load_dataset()
    training_data.prepare()

    testing_data = train_mask_rcnn.BrailleDataSet()
    testing_data.load_dataset(is_train=False)
    testing_data.prepare()

    config = train_mask_rcnn.BrailleConfig()

    model = MaskRCNN(mode="inference", model_dir="./", config=config)

    model_path = "mask_rcnn_aibl_cfg_0005.h5"
    model.load_weights(model_path, by_name=True)


    # plot predictions for train dataset
    plot_actual_vs_predicted(training_data, model, config)
    # plot predictions for test dataset
    plot_actual_vs_predicted(testing_data, model, config)
