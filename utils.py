import logging
import cv2
import numpy as np

# This file is for methods which help with calculating varying measurements and for setting different
# or designs based on class



#here I calculated the bbox width for calculations that will be needed
#in the future (in this case i needed the bbox width to draw the ellipse in the axes parameter)
#raise a value error because we need x1 to be smaller than x2 so that we can calculate a valid bbox width
# Calculating Bounding  Box width
def bbox_width(x1, x2):
    if x1 > x2:
        logging.error("x1 is greater than x2, this is an invalid bounding box")
        raise ValueError("x1 is greater than x2, this is an invalid bounding box")
    else:
        width = x2 - x1
        return width


# Calculating the coordinates of the center of the bottom of the bounding box
#we needed this calculation so that we know where to draw the arc under the player
def bbox_center_bottom(x1, y1, x2, y2):
    x_center = int((x1 + x2) / 2)
    y_bottom = int(y2)
    return x_center, y_bottom

#this class is to help us choose which pixels we want to mask and which pixels we want to mask when we process the video
class BGRHandler:
#the constructor, we are passing the frame because that is going to be needed for every instance of this class
#we also pass the creation of a list because we are going to need it created anytime we instantiate the class
    def __init__(self, frame):
        self.frame = frame
        self.BGR_values = []

    # Calculating the BGR values from the clicked pixel
    #first, we need to pass x and y coordiantes of the BGR pixel to be able to get the BGR values from it
    #second remember that the frame has 3 dimensions (height, width and channels) we need to pass the y, x to get the BGR values 
    #we have : for the BGR values because we want all three of them for the x and y coordinates.
    #the frame has the height first then the width then the channels
    def get_bgr_values(self, x, y):
        bgr_values = self.frame[y, x, :]
        return bgr_values

#this function is what is called when we click on the frame. the x gets the x coordiantes through xdata and y does the same
#we pass the x and y values from the click to our get_bgr_values to get the BGR values then we append the BGR 
#values to our list
    def click_event(self, event):
        x = int(event.xdata)
        y = int(event.ydata)
        self.BGR_values.append(
            self.get_bgr_values(x, y)
        )  # adds the BGR values to the list
        print(f"BGR values: {self.BGR_values}")
        print(f"Pixel values: {self.frame[y, x, :]}")
#this function is to get the min and max BGR values from the list of BGR values we created so that we can 
#have a range of BGR values for our mask to keep vs mask out
#we use the np.min and npmax as an easy way to get the min an max in a column (axis=0 is for column axis=1 is for row)
    def min_max_bgr_values(self):
        min_bgr_values = np.min(self.BGR_values, axis=0)
        max_bgr_values = np.max(self.BGR_values, axis=0)
        return min_bgr_values, max_bgr_values

    # Main processing function:


# process_frame(frame, model, class_colors) - Runs inference and draws annotations
# Returns the annotated frame

# Main loop:
# Keep the video reading/writing loop
# Call process_frame() for each frame

#we created this class to help us process and annotate the frames of the video so that we can see the detections and annotations on the frame
class VideoProcessor:
    #this constructor takes in the model as a parameter because we will always need to have a model set to do processing
    #we also pass the colors_dict because we want to have assigned colors for our players everytime a video is processed
    def __init__(self, model, colors_dict=None):
        self.model = model
        self.colors_dict = colors_dict

    # defining the color for different classes
    def class_color(self, class_id):
        if self.colors_dict is None:
            logging.error("color_dict is None, please define the color for each class")
            raise ValueError(
                "color_dict is None, please define the color for each class"
            )
        elif class_id not in self.colors_dict:
            logging.error(
                f"class_id {class_id} not found in color_dict, please define the color for this class"
            )
            raise ValueError(
                f"class_id {class_id} not found in color_dict, please define the color for this class"
            )
        else:
            color = self.colors_dict[class_id]
            return color

    # Draw Arc Under Player
    #this function draws an arc under the player. we pass the parameters required to draw an elipse and a frame
    #we use some caluclations we previously set in functions to draw the elipse
    
    def draw_player_arc(
        self,
        frame,
        class_id,
        x1,
        x2,
        y1,
        y2,
    ):
        width = bbox_width(x1, x2)
        center = bbox_center_bottom(x1, y1, x2, y2)
        color = self.class_color(class_id)

        cv2.ellipse(
            frame,
            center=(center),
            axes=(int(width), int(0.35 * (width))),
            angle=0,
            startAngle=-45,
            endAngle=250,
            color=color,
            thickness=2,
            lineType=cv2.LINE_4,
        )
        
    #this function is where we are running our model.predict()
    #remember that a model.predict gives you results which have information like the classes and bounding box coordinates
    #this function is running within a while loop which is looping through the frames and needs them processed one by one
    #so thats why we are processing each individual frame here
    #also, remember that if you want to use the x1y1x2y2 coordinates that come from result we need to move them to the cpu
    #then do a numpy as type int
    #zip encloses two things into a tuple so we can loop through them at the same time
    #we pass the parameters for the draw_player_arc method we created previously in this class and we get our arc
    
    def run_inference(self, frame):
        results = self.model.predict(frame)
        return results
    
    
    def process_frame(self, inference_frame, draw_frame):
        results = self.run_inference(inference_frame) 
        detections = results[0].boxes.xyxy
        detections_class = results[0].boxes.cls
        for detection, detection_class in zip(detections, detections_class):
            x1, y1, x2, y2 = detection.cpu().numpy().astype(int)
            self.draw_player_arc(draw_frame, int(detection_class), x1, x2, y1, y2)
        return draw_frame
