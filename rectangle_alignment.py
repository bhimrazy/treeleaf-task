import math
from typing import *

import cv2
import numpy as np


def read_and_resize_image(img_path: str, scale_ratio: float = 0.2) -> List[any]:
    """This function reads image from given path , crops the image
    around the rectangles and then resizes the image.

    Args:
        img_path (str): path of image
        scale_ratio (float, optional): The ratio for the image to be scaled. Defaults to 0.2.

    Returns:
        List[any]: Resized image
    """
    img = cv2.imread(
        img_path, cv2.IMREAD_UNCHANGED)  # original size (4094, 2898, 3)

    # cropping the image around the rectangles
    cropped_img = img[150:2150, 250:2700, :]  # cropped size (2000, 2450, 3)

    width = int(cropped_img.shape[1] * scale_ratio)
    height = int(cropped_img.shape[0] * scale_ratio)
    dim = (width, height)

    resized = cv2.resize(cropped_img, dim, interpolation=cv2.INTER_AREA)
    return resized


def get_contours(img) -> List:
    """Get all the contours from the image

    Args:
        img : Image array

    Returns:
        List: List of contours
    """

    if img.shape.__len__() > 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.bitwise_not(img)

    (contours, _) = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


def align(img):
    """Align all the image of rectangles

    Args:
        img : Image array
    """

    contours = get_contours(img)
    copy_img = img.copy()

    for i, c in enumerate(contours):
        # Calculate the area of each contour
        area = cv2.contourArea(c)
        # skip the contour if the area is less than 100 thresold
        if area < 100:
            continue

        (x, y, w, h) = cv2.boundingRect(c)

        # find the min area and angle of alignment of the image
        rect = cv2.minAreaRect(c)  # center , width , height and angle

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Retrieve the key parameters of the rotated bounding box
        center = (int(rect[0][0]), int(rect[0][1]))
        width = int(rect[1][0])
        height = int(rect[1][1])
        angle = int(rect[2])

        # mapping angle
        if width < height:
            angle = -(90 - angle)
        else:
            angle = angle

        # as cv2.warpAffine expects shape in (length, height)
        shape = (img.shape[1], img.shape[0])

        matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1)
        image = cv2.warpAffine(src=img, M=matrix, dsize=shape)

        copy_img[y:y+h, x:x+w] = image[y:y+h, x:x+w]

    cv2.imwrite(f'alignment.jpg', copy_img)


if __name__ == "__main__":
    image_path = "./page_2.jpg"

    # read, crop and resize image
    resized = read_and_resize_image(image_path, scale_ratio=0.25)

    # align rectangles and save image
    align(resized)
