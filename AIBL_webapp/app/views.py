from distutils.command.upload import upload
from email.mime import image
from enum import unique
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from flask import render_template
from flask import request
import sys
import uuid


from app.model import predict
from app.crop_image import crop_img
from mrcnn import visualize




def index():
    return render_template("index.html", pagename="AIBL")


def get_uuid_for_file():
    return str(uuid.uuid4())



def get_letter_count(letter_arr):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letter_dict = {k:0 for k in letters}

    for i in letter_arr:
        if i in letter_dict.keys():
            letter_dict[i] += 1

    return letter_dict

def detection():

    #Path containing folders holding original images and masked images
    uploaded_img_dir = "static/uploaded_images/"

    #Path containing all original images (i.e. images before masking)
    original_image_dir = "original_images/"

    #Path containing images after masking
    masked_image_dir = "masked_images/"


    file_uploaded = False

    if request.method == "POST":
        file_uploaded=True

        file = request.files["uploaded_file"]
        
        #Make unique folder for uploaded image
        unique_identifier = get_uuid_for_file()

        
        #Create directory to hold original image details
        original_image_dir = os.path.join(uploaded_img_dir, original_image_dir, unique_identifier)
        os.mkdir(original_image_dir)

        #Save original image to directory created above
        original_image_file_loc = os.path.join(original_image_dir, "original_image.jpg")
        file.save(original_image_file_loc)


        results = predict(original_image_file_loc)
        r = results[0]

        recoginzable_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        class_names = ["BG"] + [i for i in recoginzable_letters]

        #Read in original image
        image = plt.imread(original_image_file_loc)

        #Create directory for masked image
        this_masked_img_dir = os.path.join(uploaded_img_dir, masked_image_dir, unique_identifier)
        os.mkdir(this_masked_img_dir)

        #Location to store masked image
        masked_img_loc = os.path.join(this_masked_img_dir, "masked_image.jpg")

        #Save masked image
        visualize.save_instances(image, boxes=r["rois"], masks=r["masks"], class_ids=r["class_ids"], class_names=class_names, scores=r["scores"], path=masked_img_loc)

        #Save cropped image
        crop_img(f"{this_masked_img_dir}/")

        #Save mask plots to <this_masked_img_dir>
        get_masks_file_names = visualize.get_masks(image, r["masks"], r["rois"], class_names, r["class_ids"], path=f"{this_masked_img_dir}/")

        #
        top_masks_filenames = visualize.display_top_masks_edit(image, r["masks"], r["class_ids"], class_names, path = f"{this_masked_img_dir}/")

        #
        get_roi_filenames = visualize.get_rois(image, r["rois"], path=f"{this_masked_img_dir}/")

        letter_arr = [get_masks_file_names[i][0] for i in range(len(get_masks_file_names))]

        letter_count = get_letter_count(letter_arr)

        cropped_img_loc = os.path.join(this_masked_img_dir, "cropped.jpg")
        data = {
            "visualize": cropped_img_loc,
            "masks": get_masks_file_names,
            "top_masks": top_masks_filenames,
            "roi": get_roi_filenames,
            "letter_count": letter_arr,
            "letter_dict": letter_count
        }

        return render_template("detection.html", pagename="Detect Braille", file_uploaded=file_uploaded, data=data)

    return render_template("detection.html", pagename="Detect Braille", file_uploaded=file_uploaded)


def about():
    return render_template("about.html", pagename="About")


def login():
    return render_template("login.html", pagename="Login")

def register():
    return render_template("register.html", pagename="Register")

def tracker():
    return render_template("tracker.html", pagename="My Progress")