import cv2
import sys
import pytesseract
from matplotlib import pyplot as plt
from PIL import Image, ImageEnhance
import numpy as np
from yugidb import get_card_stat, find_card, find_card_with_id

def get_card_from_image(imPath):
    config = ('-l eng --oem 1 --psm 3')
    im = cv2.imread(imPath, cv2.IMREAD_GRAYSCALE)
    height, width = im.shape[:2]
    crop_img = im[30:70, 25:350]

    if 255 in crop_img:
        crop_img = cv2.bitwise_not(crop_img)
    
    new_image = cv2.convertScaleAbs(crop_img, alpha=3.0) # Add contrast

    text = pytesseract.image_to_string(new_image, config=config).lower().replace(',','')
    if find_card(text) == None:
        return None
    else:
        return get_card_stat(find_card(text)['id'])