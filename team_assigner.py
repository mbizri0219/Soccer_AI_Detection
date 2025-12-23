import numpy as np 
from sklearn.cluster import KMeans
from utils import player_jersey
import cv2

class Team_Assigner:
    def __init__(self, n_teams = 2):
        self.n_teams = n_teams
        self.team_kmeans = None 
        self.track_to_team_dict = {}
        self.jersey_crops = []
    
    def collect_from_frame(self, frame, detection_coordinates, detection_classes):
        for detection_coordinate, detection_class in zip(detection_coordinates, detection_classes):
            x1, y1, x2, y2 = detection_coordinate.cpu().numpy().astype(int)
            if detection_class == 2:
                crop = self.get_jersey_crop(frame, x1, y1, x2, y2)
                self.jersey_crops.append(crop)
                
    def fit_collected(self):
        self.fit(self.jersey_crops)
        self.jersey_crops.clear()
            
        
    def fit_from_detections(self, frame, detection_coordinates, detection_classes):
        """
        Collects jersey crops from detections and trains the model.
        
        frame: the video frame
        detections: the boxes.xyxy from YOLO results
        """
        jersey_crops = []
        for detection_coordinate, detection_class in zip(detection_coordinates, detection_classes):
            x1, y1, x2, y2 = detection_coordinate.cpu().numpy().astype(int)
            if detection_class == 2:
                crop = self.get_jersey_crop(frame, x1, y1, x2, y2)
                jersey_crops.append(crop)
        self.fit(jersey_crops)
    
    def get_jersey_crop(self, frame, x1, y1, x2, y2):
        """Just returns the crop, doesn't predict"""
        jx1, jy1, jx2, jy2 = player_jersey(x1, y1, x2, y2)
        return frame[jy1:jy2, jx1:jx2]

    def get_team(self, frame, x1, y1, x2, y2, track_id):
            if track_id in self.track_to_team_dict:
                return self.track_to_team_dict[track_id]
            else:
                jx1, jy1, jx2, jy2 = player_jersey(x1, y1, x2, y2)
                jersey_crop = frame[jy1:jy2, jx1:jx2]
                jersey_predict = self.predict(jersey_crop)
                self.track_to_team_dict[track_id] = jersey_predict
                return jersey_predict
    
    def get_dominant_color(self, image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_green_bound = np.array([35,40,40])
        upper_green_bound = np.array([50, 255, 255])
        green_mask = cv2.inRange(hsv_image, lower_green_bound, upper_green_bound)
        reshaped_green_mask = green_mask.reshape(-1)
        reshaped_image = image.reshape(-1, 3)
        filtered_pixels = reshaped_image[reshaped_green_mask == 0]
        kmeans = KMeans(n_clusters=2)
        if len(filtered_pixels) == 0:
            filtered_pixels = reshaped_image
        kmeans.fit(filtered_pixels)
        labels = kmeans.labels_
        counts = np.bincount(labels)
        dominant_cluster = np.argmax(counts)
        return kmeans.cluster_centers_[dominant_cluster]
        
    def fit(self, jersey_crops):
        
        colors = []
        for jersey_crop in jersey_crops:
            dominant_color = self.get_dominant_color(jersey_crop)
            print(dominant_color)
            colors.append(dominant_color)
        colors_np_array = np.array(colors)
        self.team_kmeans = KMeans(n_clusters = self.n_teams)
        self.team_kmeans.fit(colors_np_array)
        
    def predict(self, jersey_crop):
        dominant_color = self.get_dominant_color(jersey_crop)
        reshaped_dominant_color = dominant_color.reshape(1, -1)
        prediction = self.team_kmeans.predict(reshaped_dominant_color)
        return prediction[0]
        