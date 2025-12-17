import logging
import cv2
import numpy as np

# This file is for methods which help with calculating varying measurements and for setting different
# or designs based on class

# this class is to help us choose which pixels we want to mask and which pixels we want to mask when we process the video
# class BGRHandler:
#     # the constructor, we are passing the frame because that is going to be needed for every instance of this class
#     # we also pass the creation of a list because we are going to need it created anytime we instantiate the class
#     def __init__(self, frame):
#         self.frame = frame
#         self.BGR_values = []

#     # Calculating the BGR values from the clicked pixel
#     # first, we need to pass x and y coordiantes of the BGR pixel to be able to get the BGR values from it
#     # second remember that the frame has 3 dimensions (height, width and channels) we need to pass the y, x to get the BGR values
#     # we have : for the BGR values because we want all three of them for the x and y coordinates.
#     # the frame has the height first then the width then the channels
#     def get_bgr_values(self, x, y):
#         bgr_values = self.frame[y, x, :]
#         return bgr_values

#     # this function is what is called when we click on the frame. the x gets the x coordiantes through xdata and y does the same
#     # we pass the x and y values from the click to our get_bgr_values to get the BGR values then we append the BGR
#     # values to our list
#     def click_event(self, event):
#         x = int(event.xdata)
#         y = int(event.ydata)
#         self.BGR_values.append(
#             self.get_bgr_values(x, y)
#         )  # adds the BGR values to the list
#         print(f"BGR values: {self.BGR_values}")
#         print(f"Pixel values: {self.frame[y, x, :]}")

#     # this function is to get the min and max BGR values from the list of BGR values we created so that we can
#     # have a range of BGR values for our mask to keep vs mask out
#     # we use the np.min and npmax as an easy way to get the min an max in a column (axis=0 is for column axis=1 is for row)
#     def min_max_bgr_values(self):
#         min_bgr_values = np.min(self.BGR_values, axis=0)
#         max_bgr_values = np.max(self.BGR_values, axis=0)
#         return min_bgr_values, max_bgr_values


    # Main processing function:


# process_frame(frame, model, class_colors) - Runs inference and draws annotations
# Returns the annotated frame

# Main loop:
# Keep the video reading/writing loop
# Call process_frame() for each frame


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