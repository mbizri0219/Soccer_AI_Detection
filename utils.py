import logging

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

#defining the color for different classes
def class_color(class_id, color_dict=None):
    if color_dict is None:
        logging.error("color_dict is None, please define the color for each class")
        raise ValueError("color_dict is None, please define the color for each class")
    elif class_id not in color_dict:
        logging.error(f"class_id {class_id} not found in color_dict, please define the color for this class")
        raise ValueError(f"class_id {class_id} not found in color_dict, please define the color for this class")
    else:
        color = color_dict.get(class_id)
        return color

#Draw Arc Under Player
def draw_player_arc(frame, center, radius, start_angle, end_angle, color, thickness=2, angle=0, x1, x2, y1, y2):
    width = bbox_width(x1, x2)
    center = bbox_center_bottom(x1, y1, x2, y2)
    color = class_color(class_id)
    
           cv2.ellipse(
            frame, 
            center=(center), 
            axes=int(width), int(.35*(width)), 
            angle=0,
            startAngle=-45, 
            endAngle=250, 
            color=color, 
            thickness=2,
            lineType=cv2.LINE_4)
    
    
    # Main processing function:

# process_frame(frame, model, class_colors) - Runs inference and draws annotations
# Returns the annotated frame

# Main loop:
# Keep the video reading/writing loop
# Call process_frame() for each frame

class VideoProcessor:
    def __init__()
    