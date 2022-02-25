
from numpy import expand_dims
from numpy import mean

from mrcnn.utils import compute_ap
from mrcnn.model import load_image_gt
from mrcnn.model import mold_image
from mrcnn.model import MaskRCNN
import train_mask_rcnn





def evaluate_rcnn_model(data_set, model, config):
    '''
    Calculate mean average precision for model on dataset
    '''
    APs = []
    for image_id in data_set.image_ids:
        #load image, bounding boxes and masks fr the image
        #image, image_meta, gt_class, gt_bbox, gt_mask = load_image_gt(data_set, config, image_id, use_mini_mask=False)
        image, image_meta, gt_class_id, gt_bbox, gt_mask = load_image_gt(data_set, config, image_id, use_mini_mask=False)
        print(len(image))
        #Convert pixel values
        scaled_img = mold_image(image, config)

        #Convert image into one sample
        sample = expand_dims(scaled_img, 0)

        #make prediction
        yhat = model.detect(sample, verbose=0)

        #Extract results for first sample
        r = yhat[0]

        #Calculate stats inc AP
        AP, _, _, _ = compute_ap(gt_bbox, gt_class_id, gt_mask, r["rois"], r["class_ids"], r["scores"], r["masks"])

        #Append to APs arr
        APs.append(AP)

    #Calculate mean avg precision 
    mean_avg_precision = mean(APs)

    return mean_avg_precision





if __name__ == "__main__":
    #load training data set
    training_data = train_mask_rcnn.BrailleDataSet()
    training_data.load_dataset()
    training_data.prepare()

    #Load training dataset
    testing_data = train_mask_rcnn.BrailleDataSet()
    testing_data.load_dataset(is_train=False)
    testing_data.prepare()

    config = train_mask_rcnn.BrailleConfig()

    #define model
    model = MaskRCNN(mode="inference", model_dir="./", config=config)

    #load model weights
    model.load_weights("aibl_cfg20220407T1716/mask_rcnn_aibl_cfg_0005.h5", by_name=True)

    #Evaluate model on training_data 
    train_mean_avg_precision = evaluate_rcnn_model(training_data, model, config)

    #Evaluate model on testing_data
    test_mean_avg_precision = evaluate_rcnn_model(testing_data, model, config)

    print(f"Training mean avg precision:\n{str(train_mean_avg_precision)}")
    print(f"Testing mean average precision:\n{str(test_mean_avg_precision)}")

    



