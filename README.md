WRITTEN BY ME:

The following goes through the project step by step, more detailed information about code syntax will be available in the code itself but this is a guide for the overarching steps taken to do this project

Goal:

    First lets look at the goal of the project from an overhead view. The goal of this project is to annotate and extrapolate information about a video of a football game by utilizing AI and object detection.

Choosing model:

    a- Since we are using object detection, we first choose the object detection model. YOLO (you only look once), it is a one stage model which takes an image, creates an SxS grid which then gets used to create bounding boxes with IoU scores on objects and a class probability map for each cell in the SxS grid. After combining the class probability map with the bounding boxes it gives us its prediction.

    b- When approaching this kind of project the first thing you want to do is see if there is a pre-trained model that you can utilize and fine-tune. We want to use it as a "base" for the project to build on. It requires a lot of data to train a model from scratch. Furthermore, a pretrained model gives you a good starting point with a lot of general knowledge which you can then fine-tune for your specific task. This is ideal because you dont want it to be overfitted on one task because it was only trained on how to detect one specific thing. YOLO has a model pretrained on the COCO dataset (Common Objects in Context — a large dataset with 80+ object classes including "person" and "sports ball"). We will be using yolov8n.pt as the base for this project.

Inferencing:

    a- Now that we have our base, we want to run an inference on yolov8n.pt. This is done by doing model.predict(yolov8n). Remember that anytime you use model.predict the frames are in BGR format which is openCVs format for colors. We need to convert to RGB to plot with matplotlib. Also remember that the inference gives us a list of results and we want to access the first result object (results[0]) to get the detections from the first frame

    b-After running the inference we notice that the detection isn't as good as it should be. It surely is good as a base but we need to fine tune things so that we get better precision and recall (which will be explained in a bit).

Dataset:

    a- Anytime someone tells you to train a model the first thing your mind should go to is "DATA". You need good labelled data to train a model. Gathering and labelling the data is debatably the hardest part of this entire process.

    b- when it comes to gathering and labelling data there are certain things to make sure of:

        i-the pictures need to contain the objects you are detecting for but also need to contain more than just the object. for example, we are detecting for players but we dont want to just have a bunch of zoomed up pictures of just a player to train our model on. We want pictures of players in different settings, from different angles and with other things in the picture.

        ii- you will have one folder for the images and another folder within the same directory file hierarchy for the labels. The labels will be .txt but must have the same name as the corresponding image for the label. As an example, in our test datasetwe have two folders, images and labels. in the images folder the image: 4b770a_1_4_png.rf.5a45b3b841a06de414ceb802e34c136f.jpg corresponds to the txt file in the labels folder named:4b770a_1_4_png.rf.5a45b3b841a06de414ceb802e34c136f.txt.

        iii- in the label files (open one of the label files Training_Dataset\test\labels) you will notice some weird syntax. The .txt file contains all the detections for that image where each line is a single detection. In each detection, the first number indicates the class of the detection (how the class is defined will be explained shortly), the next 4 number values are (x_center, y_center, width height) all normalized between 0-1 relative to image dimensions.

        iiii- to point to all the data in your dataset you need to make a .yaml file. The .yaml file gives the program the information it needs to complete each step of the fine tuning. It starts by telling the program the path to your dataset. It then states the number of classes being detected, the names of all the classes (WITH THE INDEX FOR EACH CLASS WHICH IS HOW OUR LABEL FILES ARE LABELING THE CLASS OF EACH DETECTION.) the dataset splits for train, validate and test.

        iiiii- as a reminder:
            the train dataset is what we are train the model on (in this case fine tuning), this is the data our model learns from for future inferences.

            the validation dataset is also considered a part of the fine tuning process but our model is not learning from this data. it uses this data to fine tune its hyperparameters(things like batch size and learning rate)

Fine tuning / training:

    a- first, before you start fine tuning and training you need to make sure you know what GPU / CPU is currently configured on your device to be used for training. Make sure your program is using the intended processor

    b- next we load and train the model and set our hyperParameters for the train. Discussion of the hyperparameters will be in the code base. We run the fine-tuning and receive a plethora of files. best.pt ,last.pt, and a bunch of graphs. best.pt is our best run and last.pt is our last run. Our last run isnt always the best run we had, remember to keep that in mind.

    c- We want to look at the graphs that were produced by our train to see the best confidence score to use for the inference, the precision, recall and to make sure our model is doing a good job predicting. I explain my analysis of the graphs in the codebase

    d- We then want to do another inference, model.predict(), to see how our fine-tuned model compares to the base model we previously used in a prediction. This is done by doing another inference that uses the best.pt from our train. In this example our detections were more accurate than they were before we did the fine tune
