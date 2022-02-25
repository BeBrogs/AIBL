'''
Split the braille data set into training and testing sets

'''





#imports
from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from mrcnn.utils import Dataset
from mrcnn.visualize import display_instances
from mrcnn.utils import extract_bboxes
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
from subprocess import check_output as sp_out
from matplotlib import pyplot as plt





class BrailleDataSet(Dataset):
    '''
    Define and load the braille dataset
    '''
    

    #def __init__(self):
        #All braille letters being accounted for


    def load_dataset(self, dir="BRAILLE", is_train=True):
        self.__braille_letters ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        #Define all appropriate classes
        for enum, i in enumerate(self.__braille_letters):
            self.add_class("dataset", enum+1, i)


        

        #Define data locations
        #Define images directory
        images_dir = "BRAILLE/numbered_images/"

        #Define XML annotations directory
        annots_dir = "BRAILLE/numbered_annots/"


        #All files in images/ dir
        all_image_files = sp_out(f"ls {images_dir}", shell=True).decode("utf-8")
        
        all_image_files_split = all_image_files.split("\n")

        total_num_files = len(all_image_files_split)

        num_of_training_files = total_num_files *.9
        num_of_testing_files = total_num_files *.1

        #FIND ALL IMAGES 
        for f in all_image_files_split:
            if f == "":
                pass
            else:
                #Get file unique id
                f_id = f[:-4]
                #print(f_id)


                #Skip over bad images
                if f_id in ["00090"]:
                    continue

        
            #Skip the remaining 10% of all files, these will be used for the test dataset
            if is_train and int(f_id) >= num_of_training_files:
                continue
        

            if not is_train and int(f_id) < num_of_training_files:
                continue


            image_path = images_dir + f
            ann_path = annots_dir + f_id + ".xml"
            #Add to dataset
            self.add_image("dataset", image_id=f_id, path=image_path, annotation=ann_path, class_ids=[int(i) for i in range(len(self.__braille_letters)+1)])
    

    def extract_bounding_boxes(self,f):
        '''
        Extract the bounding boxes from XML annotation file
        '''
        print("EXTRACTING")
        #load and parse file
        tree = ElementTree.parse(f)

        #Get root of XML file
        root = tree.getroot()

        #List to be populated with bounding box details
        bounding_box_list = []
        
        self.__braille_letters ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        for bbox in root.findall(".//object"):
            obj_name = bbox.find("name").text
            x_min = int(bbox.find("./bndbox/xmin").text)
            y_min = int(bbox.find("./bndbox/ymin").text)
            x_max = int(bbox.find("./bndbox/xmax").text)
            y_max = int(bbox.find("./bndbox/ymax").text)
            if obj_name in self.__braille_letters:
                bounding_box_list.append([x_min, y_min, x_max, y_max, obj_name])

        #Get image dimensions
        width = int(root.find(".//size/width").text)
        height = int(root.find(".//size/height").text)
        print(bounding_box_list)

        return bounding_box_list, width, height

    def load_mask(self, image_id):
        '''
        Load the masks for an image
        '''


        #get details of image
        info = self.image_info[image_id]
        print(info)

        #Define box file location
        path = info["annotation"]

        #load XML
        boxes, w, h = self.extract_bounding_boxes(path)


        #create one array for all masks, each on different channel
        masks = zeros([h,w,len(boxes)], dtype="uint8")


        #create masks
        class_ids = []
        for i in range(len(boxes)):
            box = boxes[i]
            row_s, row_e = box[1], box[3]
            col_s, col_e = box[0], box[2]
            print(box[4])
            if box[4] == "A":
                masks[row_s:row_e, col_s:col_e, i] =1 
                class_ids.append(self.class_names.index("A"))
            
            elif box[4] == "B":
                masks[row_s: row_e,col_s:col_e, i] = 2
                class_ids.append(self.class_names.index("B"))
            
            elif box[4] == "C":
                masks[row_s:row_e, col_s:col_e, i] = 3
                class_ids.append(self.class_names.index("C"))
            
            elif box[4] == "D":
                masks[row_s: row_e, col_s:col_e, i] = 4
                class_ids.append(self.class_names.index("D"))
            
            elif box[4] == "E":
                masks[row_s: row_e, col_s:col_e, i] = 5
                class_ids.append(self.class_names.index("E"))
            
            elif box[4] == "F":
                masks[row_s: row_e, col_s:col_e, i] = 6
                class_ids.append(self.class_names.index("F"))
            
            elif box[4] == "G":
                masks[row_s:row_e, col_s:col_e, i] = 7
                class_ids.append(self.class_names.index("G"))

            elif box[4] == "H":
                masks[row_s:row_e, col_s:col_e, i] = 8
                class_ids.append(self.class_names.index("H"))

            elif box[4] == "I":
                masks[row_s:row_e, col_s:col_e, i] = 9
                class_ids.append(self.class_names.index("I"))

            elif box[4] == "J":
                masks[row_s:row_e, col_s:col_e, i] = 10
                class_ids.append(self.class_names.index("J"))

            elif box[4] == "K":
                masks[row_s:row_e, col_s:col_e, i] = 11
                class_ids.append(self.class_names.index("K"))

            elif box[4] == "L":
                masks[row_s:row_e, col_s:col_e, i] = 12
                class_ids.append(self.class_names.index("L"))

            elif box[4] == "M":
                masks[row_s:row_e, col_s:col_e, i] = 13
                class_ids.append(self.class_names.index("M"))

            elif box[4] == "N":
                masks[row_s:row_e, col_s:col_e, i] = 14
                class_ids.append(self.class_names.index("N"))

            elif box[4] == "O":
                masks[row_s:row_e, col_s:col_e, i] = 15
                class_ids.append(self.class_names.index("O"))

            elif box[4] == "P":
                masks[row_s:row_e, col_s:col_e, i] = 16
                class_ids.append(self.class_names.index("P"))

            elif box[4] == "Q":
                masks[row_s:row_e, col_s:col_e, i] = 17
                class_ids.append(self.class_names.index("Q"))

            elif box[4] == "R":
                masks[row_s:row_e, col_s:col_e, i] = 18
                class_ids.append(self.class_names.index("R"))

            elif box[4] == "S":
                masks[row_s:row_e, col_s:col_e, i] = 19
                class_ids.append(self.class_names.index("S"))

            elif box[4] == "T":
                masks[row_s:row_e, col_s:col_e, i] = 20
                class_ids.append(self.class_names.index("T"))

            elif box[4] == "U":
                masks[row_s:row_e, col_s:col_e, i] = 21
                class_ids.append(self.class_names.index("U"))

            elif box[4] == "V":
                masks[row_s:row_e, col_s:col_e, i] = 22
                class_ids.append(self.class_names.index("V"))

            elif box[4] == "W":
                masks[row_s:row_e, col_s:col_e, i] = 23
                class_ids.append(self.class_names.index("W"))

            elif box[4] == "X":
                masks[row_s:row_e, col_s:col_e, i] = 24
                class_ids.append(self.class_names.index("X"))

            elif box[4] == "Y":
                masks[row_s: row_e, col_s:col_e, i] = 25
                class_ids.append(self.class_names.index("Y"))

            elif box[4] == "Z":
                masks[row_s:row_e, col_s:col_e, i] = 26
                class_ids.append(self.class_names.index("Z"))



        return masks, asarray(class_ids, dtype="int32")


    def image_reference(self, image_id):
        info = self.image_info[image_id]
        return info["path"]


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

if __name__ == "__main__":
    #Training data set
    training_data = BrailleDataSet()
    training_data.load_dataset()
    training_data.prepare()
    print(f"Train: {str(len(training_data.image_ids))}")


    #Testing data set
    testing_data = BrailleDataSet()
    testing_data.load_dataset(is_train=False)
    testing_data.prepare()
    print(f"Test: {str(len(testing_data.image_ids))}")


    #Prepare config
    config = BrailleConfig()
    config.display()

    #Defining the model 
    model = MaskRCNN(mode="training", model_dir="./", config=config)
    
    #Loading weights
    model.load_weights("mask_rcnn_coco.h5", by_name=True, exclude=["mrcnn_class_logits", "mrcnn_bbox_fc",  "mrcnn_bbox", "mrcnn_mask"])

    model.train(training_data, testing_data, learning_rate=config.LEARNING_RATE, epochs=5, layers="heads")
