import logging
import cv2
import numpy as np
#This file is for methods which help with calculating varying measurements and for setting different 
# or designs based on class


#Calculating Bounding  Box width
def bbox_width(x1, x2):
    if x1 > x2:
        logging.error("x1 is greater than x2, this is an invalid bounding box")
        raise ValueError("x1 is greater than x2, this is an invalid bounding box")
    else:
        width = x2 - x1
        return width
    
    
#Calculating the coordinates of the center of the bottom of the bounding box
def bbox_center_bottom(x1, y1, x2, y2):
    x_center = int((x1 + x2) / 2)
    y_bottom = int(y2)
    return x_center, y_bottom


class BGRHandler:
    
    def __init__(self, frame):
        self.frame = frame
        self.BGR_values = []
        

    def click_event(self, event):
        x = int(event.xdata)
        y = int(event.ydata)
        self.BGR_values.append(self.get_bgr_values(x, y)) #adds the BGR values to the list
        print(f"BGR values: {self.BGR_values}")
        print(f"Pixel values: {self.frame[y, x, :]}")

    #Calculating the BGR values from the clicked pixel
    def get_bgr_values(self, x, y):
        bgr_values = self.frame[y, x, :]
        return bgr_values
    
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

class VideoProcessor:
    def __init__(self, model, colors_dict=None):
        self.model = model
        self.colors_dict = colors_dict
    
    #defining the color for different classes
    def class_color(self, class_id):
        if self.colors_dict is None:
            logging.error("color_dict is None, please define the color for each class")
            raise ValueError("color_dict is None, please define the color for each class")
        elif class_id not in self.colors_dict:
            logging.error(f"class_id {class_id} not found in color_dict, please define the color for this class")
            raise ValueError(f"class_id {class_id} not found in color_dict, please define the color for this class")
        else:
            color = self.colors_dict[class_id]
            return color
    
    #Draw Arc Under Player
    def draw_player_arc(self, frame, class_id, x1, x2, y1, y2, thickness=2):
        width = bbox_width(x1, x2)
        center = bbox_center_bottom(x1, y1, x2, y2)
        color = self.class_color(class_id)
        
        cv2.ellipse(
        frame, 
        center=(center), 
        axes=(int(width), int(.35*(width))), 
        angle=0,
        startAngle=-45, 
        endAngle=250, 
        color=color, 
        thickness=2,
        lineType=cv2.LINE_4)
        
    def mask_frame(self, frame):
        mask = np.zeros_like(frame)
        return mask
    
    def process_frame(self, frame):
        results = self.model.predict(frame)
        detections = results[0].boxes.xyxy
        detections_class = results[0].boxes.cls
        for detection, detection_class in zip(detections, detections_class):
            x1, y1, x2, y2 = detection.cpu().numpy().astype(int)
            self.draw_player_arc(frame, int(detection_class), x1, x2, y1, y2)
        return frame