import cv2
import math
import numpy as np
from typing import *


def read_and_resize_image(img_path: str, scale_ratio: float = 0.2) -> List[any]:
    """This function reads image from given path , crops the image 
    around the rectangles and then resizes the image.

    Args:
        img_path (str): path of image
        scale_ratio (float, optional): The ratio for the image to be scaled. Defaults to 0.2.

    Returns:
        List[any]: Array of resized image
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


def get_corners(img, max_corners: int = 24):
    """This function finds all the corners coordiantes of rectangles and lines from the image.

    Since in the image, we have 4 recatngles and 2 lines i.e 4*4 + 4*2 = 24 corners

    Args:
        img : Array of image
        max_corners (int, optional): Max amount of corners to track. Defaults to 24.

    Returns:
        _type_: _description_
    """
    if img.shape.__len__() > 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = np.float32(img)
    corners = cv2.goodFeaturesToTrack(img, max_corners, 0.01, 10)
    corners = np.int0(corners)
    corners = [a.tolist() for a in corners.reshape(max_corners, 2)]
    return corners


def get_rectangle_contours(img) -> List[List[int]]:
    """This function finds the bounding box for all the rectangles i.e 4 and 
    returns the coordiantes of the bounding box in (x, y, w, h) format.

    Args:
        img : Array of image

    Returns:
        List[List[int]]: Coordiantes of the bounding box
    """

    if img.shape.__len__() > 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.bitwise_not(img)

    (contours, _) = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    rectangles = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if area > 50:
            rectangles.append((x, y, w, h))
    return rectangles


def generate_numbers_on_image(img, rectangles, corners) -> None:
    """Generating numbers on the image below the rectangles as per the length of lines
    from 1 to 4.

    And generates the final image with name numbering.png

    Args:
        img (_type_): Array of image
        rectangles (_type_): Array of rectangles coordiantes
        corners (_type_): Array of all the corners coordinates
    """

    # finding the length of line for each rectangles

    lengths = {}
    for rect in rectangles:
        (x, y, w, h) = rect
        c = [x+w//2, y+h//2]  # center of rectangle

        # filter the points that are closest to the center of rectangles
        filtered = list(filter(lambda x: math.dist(c, x) < w, corners))

        # mapping points with their distances from center
        ps = {int(math.dist(c, p)): p for p in filtered}
        ps = dict(sorted(ps.items()))

        # two closest points from the center is the coordinate of line
        l1, l2 = list(ps.values())[:2]

        # length of line
        d = int(math.dist(l1, l2))
        lengths[d] = rect

    # sorting as per the length of the line
    lengths = dict(sorted(lengths.items()))

    # writing numbers on the image
    i = 1
    for k, v in lengths.items():

        font = cv2.FONT_HERSHEY_SIMPLEX  # font

        (x, y, w, h) = v
        org = (x+45, y+h+30)  # position of text

        # fontScale
        fontScale = 1
        # Blue color in BGR
        color = (0, 0, 255)
        # Line thickness of 2 px
        thickness = 2

        # putting text on the image
        cv2.putText(img, f'{i}', org, font,
                    fontScale, color, thickness, cv2.LINE_AA)
        i += 1

    print("Generating final numbered image....")
    cv2.imwrite('numbering.png', img)


if __name__ == "__main__":
    image_path = "./page_2.jpg"

    # read, crop and resize image
    resized = read_and_resize_image(image_path, scale_ratio=0.25)

    # get bounding box of the rectangles i.e 4 rectangles
    rects = get_rectangle_contours(resized)

    # get corners coordinates of all the shapes i.e 24 corners
    corners = get_corners(resized)

    generate_numbers_on_image(img=resized, rectangles=rects, corners=corners)
