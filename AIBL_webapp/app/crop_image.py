from PIL import Image, ImageOps
from numpy import asarray, array
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os


def get_row_crop(img_np):
    midpoint = len(img_np[0])//2

    for enum, i in enumerate(img_np):
        if i[midpoint] != 255:
            return enum


def get_col_crop(img_np, width):
    middle_row = width//2

    for enum, i in enumerate(img_np[middle_row]):
        if int(i) < 250:
            return enum

def get_gray_img_np_arr(img_path):
    img = Image.open(img_path)
    gray_image = ImageOps.grayscale(img)

    img_np = asarray(gray_image)
    return img_np

def crop_img(img_path):
    jpg_path = os.path.join(img_path, "masked_image.jpg")
    image = cv2.imread(jpg_path)
    row, col, color = image.shape
    img_np = get_gray_img_np_arr(jpg_path)
    row_crop = get_row_crop(img_np)
    col_crop = get_col_crop(img_np, col)
    np_img = array(image)
    
    cropped_img = np_img[row_crop+1: row-row_crop, col_crop: col-col_crop]

    #convert array to image
    image = Image.fromarray(cropped_img)
    image.save(os.path.join(img_path, "cropped.jpg"))

if __name__=="__main__":
    path = os.path.join("..", "static", "uploaded_images", "masked_images", "f2b0ec2d-148b-43e2-93cf-7510ddeaeadd")
    print(path)
    
    #crop_img("../static/uploaded_images/masked_images/f2b0ec2d-148b-43e2-93cf-7510ddeaeadd/")
    crop_img(path)