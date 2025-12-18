import numpy as np 
from sklearn.cluster import KMeans
from utils import player_jersey

class Team_Assigner:
    def __init__(self, n_teams = 2):
        self.n_teams = n_teams
        self.team_kmeans = None 
    
    def fit_from_detections(self, frame, detections):
        """
        Collects jersey crops from detections and trains the model.
        
        frame: the video frame
        detections: the boxes.xyxy from YOLO results
        """
        jersey_crops = []
        for detection in detections:
            x1, y1, x2, y2 = detection.cpu().numpy().astype(int)
            crop = self.get_jersey_crop(frame, x1, y1, x2, y2)
            jersey_crops.append(crop)
        
        self.fit(jersey_crops)
    
    def get_jersey_crop(self, frame, x1, y1, x2, y2):
        """Just returns the crop, doesn't predict"""
        jx1, jy1, jx2, jy2 = player_jersey(x1, y1, x2, y2)
        return frame[jy1:jy2, jx1:jx2]

    def get_team(self, frame, x1, y1, x2, y2):
        jx1, jy1, jx2, jy2 = player_jersey(x1, y1, x2, y2)
        jersey_crop = frame[jy1:jy2, jx1:jx2]
        return self.predict(jersey_crop)
    
    def get_dominant_color(self, image):
        reshaped_image = image.reshape(-1, 3)
        kmeans = KMeans(n_clusters=2)
        kmeans.fit(reshaped_image)
        labels = kmeans.labels_
        counts = np.bincount(labels)
        dominant_cluster = np.argmax(counts)
        return kmeans.cluster_centers_[dominant_cluster]
        
    def fit(self, jersey_crops):
        
        colors = []
        for jersey_crop in jersey_crops:
            dominant_color = self.get_dominant_color(jersey_crop)
            colors.append(dominant_color)
        colors_np_array = np.array(colors)
        self.team_kmeans = KMeans(n_clusters = self.n_teams)
        self.team_kmeans.fit(colors_np_array)
        
    def predict(self, jersey_crop):
        dominant_color = self.get_dominant_color(jersey_crop)
        reshaped_dominant_color = dominant_color.reshape(1, -1)
        prediction = self.team_kmeans.predict(reshaped_dominant_color)
        return prediction[0]
        