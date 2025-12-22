#This file will have hardcoded values and important paths to make it easy to find and change them

class Config:
    #this is where we set the class colors dictionary for our classes
    CLASS_COLORS ={0: (0, 0, 255), 1: (0, 255, 0), 2: (255, 0, 0), 3:(0, 255, 255)}
    TEAM_COLORS = {0: (255, 0, 0), 1: (0, 0, 255)}
    #Class Names Dictionary
    CLASS_NAMES = {0:'ball' , 1:'goalkeeper', 2:'player', 3:'referee'}

    #input video path
    INPUT_VIDEO_PATH='input-videos/08fd33_4.mp4'

    #Model Path
    MODEL_PATH='train64/weights/best.pt'

    #Output Video Path 
    OUTPUT_VIDEO_PATH = "output.mp4"

    #Video Settings

    #Output FPS
    OUTPUT_FPS=20.0

    #Codec
    CODEC='mp4v'