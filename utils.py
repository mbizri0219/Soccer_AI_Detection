import logging
import cv2
import numpy as np

# This file is for methods which help with calculating varying measurements and for setting different
# or designs based on class

def player_jersey(x1,y1,x2,y2):
    height = y2 - y1
    y_top = y1 + int(height * 0.25)     # 25% down from top
    y_bottom = y1 + int(height * 0.5)   # 50% down from top (middle)
    return x1,y_top,x2,y_bottom


# here I calculated the bbox width for calculations that will be needed
# in the future (in this case i needed the bbox width to draw the ellipse in the axes parameter)
# raise a value error because we need x1 to be smaller than x2 so that we can calculate a valid bbox width
# Calculating Bounding  Box width
def bbox_width(x1, x2):
    if x1 > x2:
        logging.error("x1 is greater than x2, this is an invalid bounding box")
        raise ValueError("x1 is greater than x2, this is an invalid bounding box")
    else:
        width = x2 - x1
        return width


# Calculating the coordinates of the center of the bottom of the bounding box
# we needed this calculation so that we know where to draw the arc under the player
def bbox_center_bottom(x1, y1, x2, y2):
    x_center = int((x1 + x2) / 2)
    y_bottom = int(y2)
    return x_center, y_bottom