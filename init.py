import cv2
from flask import Flask
from flask_cors import CORS

app = Flask("DNSRServer")
cors = CORS(app, supports_credentials=True)

AGE_CAFFE = "ageData/age_net.caffemodel" #caffe is a deep learning framework: this being the knwoledge/memory
AGE_PROTO = "ageData/deploy_age.prototxt" #prototxt is like the recipe for everything: the lego build manual
FACE_CAFFE = "faceData/face_net.caffemodel"
FACE_PROTO = "faceData/deploy_face.prototxt"
GENDER_CAFFE = "genderData/gender_net.caffemodel"
GENDER_PROTO = "genderData/deploy_gender.prototxt"
GENDER_LIST = ['Male','Female']
GENDER_DICT = {"Male":(255,0,0),"Female":(255,0,203)}

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746) #RGB subtract 
#gonna use both for gender and age just cuz

AGE_POINTS = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
                 '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)'] #age ranges of this model 
# EXPAND AGE RANGES LATER !!!!

face_net = cv2.dnn.readNetFromCaffe(FACE_PROTO, FACE_CAFFE) #dnn = deep neural network
age_net = cv2.dnn.readNetFromCaffe(AGE_PROTO,AGE_CAFFE)
gender_net = cv2.dnn.readNetFromCaffe(GENDER_PROTO,GENDER_CAFFE)

frame_width = 1280
frame_height = 720

# Face Detection Function: Defines a function get_faces() which takes a frame (image) as input and detects faces within it. 
# It utilizes the pre-trained face detection model (face_net) to detect faces with a confidence threshold of 0.5.

# Processing Detected Faces: Extracts the bounding box coordinates for each detected face and adjusts them slightly for better visualization.
# These coordinates represent the region of interest (ROI) where faces are detected within the frame.

# Output: Returns a list of tuples containing coordinates of bounding boxes for each detected face within the input frame. 
# Each tuple represents the (start_x, start_y, end_x, end_y) coordinates of the bounding box surrounding a detected face.

