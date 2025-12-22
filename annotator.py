import cv2
import logging
from utils import bbox_width, bbox_center_bottom
            
class Annotator:

    def __init__(self, colors_dict, team_color):
        self.colors_dict = colors_dict
        self.team_color = team_color
    
    # defining the color for different classes
    def get_class_color(self, class_id):
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
        
    def get_team_color(self, team_id):
        
        if team_id is None:
            return [0,0,0]
        
        elif self.team_color is None:
            logging.error("team_color is None, please define the color for each class")
            raise ValueError(
                "team_color is None, please define the color for each class"
            )
        elif team_id not in self.team_color:
            logging.error(
                f"class_id {team_id} not found in team_color, please define the color for this class"
            )
            raise ValueError(
                f"team_id {team_id} not found in team_color, please define the color for this class"
            )
        else:
            color = self.team_color[team_id]
            return color            
          # Draw Arc Under Player
    # this function draws an arc under the player. we pass the parameters required to draw an elipse and a frame
    # we use some caluclations we previously set in functions to draw the elipse

    def draw_player_arc(
        self,
        frame,
        class_id,
        x1,
        x2,
        y1,
        y2,
        track_id=None,
        team=None
    ):
        width = bbox_width(x1, x2)
        center = bbox_center_bottom(x1, y1, x2, y2)
        color = [0, 0, 0]
        if class_id == 2:
            color = self.get_team_color(team)
        else:
            color = self.get_class_color(class_id)

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

        rectangle_width = 40
        rectangle_height = 20
        x1_rect = center[0] - rectangle_width // 2
        x2_rect = center[0] + rectangle_width // 2
        y1_rect = (y2 - rectangle_height // 2) + 15
        y2_rect = (y2 + rectangle_height // 2) + 15

        if track_id is not None:
            cv2.rectangle(
                frame,
                (int(x1_rect), int(y1_rect)),
                (int(x2_rect), int(y2_rect)),
                color,
                cv2.FILLED,
            )
            
            # figuring out the text size
            text_size = cv2.getTextSize(f"{track_id}", cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            text_x = int((center[0]) - (text_size[0] // 2))
            text_y = int(((y1_rect + y2_rect) // 2) + (text_size[1] // 2))
            
            cv2.putText(
                frame,
                f"{track_id}",
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                2,
            )

