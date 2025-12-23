import cv2 
from ultralytics import YOLO
from config import Config 
from annotator import Annotator
from videoprocessor import VideoProcessor
from team_assigner import Team_Assigner

#when loading a video we want to use videocapture
cap = cv2.VideoCapture(Config.INPUT_VIDEO_PATH)

# Get the default frame width and height this is important for when we write the output video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*Config.CODEC)
out = cv2.VideoWriter(Config.OUTPUT_VIDEO_PATH, fourcc, Config.OUTPUT_FPS, (frame_width, frame_height))
#the model we are using which is the best.pt model that we trained on our personal dataset
model = YOLO(Config.MODEL_PATH)

annotator = Annotator(Config.CLASS_COLORS, Config.TEAM_COLORS)
team_assigner = Team_Assigner()
videoprocessor = VideoProcessor(model, annotator, team_assigner)

for i in range(21):
    ret, frame = cap.read()
    results = model.predict(frame)
    detection_classes = results[0].boxes.cls                            
    detection_coordinates = results[0].boxes.xyxy
    team_assigner.collect_from_frame(frame, detection_coordinates, detection_classes)
team_assigner.fit_collected()
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)



while True:
    #cap.read() gives us 2 pieces of information. a ret flag which tells us if the video is still going
    #and the frame which is the actual frame that we are processing
    ret, frame = cap.read()
    #so if the video is done we want to close the file. we want this check first
    if not ret:
        print("Finished reading video file. Exiting...")
        break
    annotated_frame = videoprocessor.process_frame(frame, frame)
    out.write(annotated_frame)
cap.release()
out.release()