import numpy as np

# we created this class to help us process and annotate the frames of the video so that we can see the detections and annotations on the frame
class VideoProcessor:
    # this constructor takes in the model as a parameter because we will always need to have a model set to do processing
    # we also pass the colors_dict because we want to have assigned colors for our players everytime a video is processed
    def __init__(self, model, annotator, team_assigner):
        self.model = model
        self.annotator = annotator
        self.team_assigner = team_assigner

    # this function is where we are running our model.predict()
    # remember that a model.predict gives you results which have information like the classes and bounding box coordinates
    # this function is running within a while loop which is looping through the frames and needs them processed one by one
    # so thats why we are processing each individual frame here
    # also, remember that if you want to use the x1y1x2y2 coordinates that come from result we need to move them to the cpu
    # then do a numpy as type int
    # zip encloses two things into a tuple so we can loop through them at the same time
    # we pass the parameters for the draw_player_arc method we created previously in this class and we get our arc

    def run_inference(self, frame):
        results = self.model.predict(frame)
        return results

    def run_tracker(self, frame):
        results = self.model.track(frame, tracker="bytetrack.yaml", persist=True)
        return results

    def process_frame(self, inference_frame, draw_frame):
        results = self.run_tracker(inference_frame)
        detections = results[0].boxes.xyxy
        detections_class = results[0].boxes.cls
        if results[0].boxes.id is not None:
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            for track_id, detection, detection_class in zip(
                track_ids, detections, detections_class):
                
                x1, y1, x2, y2 = detection.cpu().numpy().astype(int)
                assigned_team= self.team_assigner.get_team(draw_frame, x1, y1, x2, y2, track_id)
                
                self.annotator.draw_player_arc(draw_frame, int(detection_class), x1, x2, y1, y2, track_id, assigned_team)                
        else:
            for detection, detection_class in zip(detections, detections_class):
                x1, y1, x2, y2 = detection.cpu().numpy().astype(int)            
                self.annotator.draw_player_arc(draw_frame, int(detection_class), x1, x2, y1, y2)
        return draw_frame
