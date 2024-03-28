from init import face_net
import cv2
import numpy as np

# get faces function
def get_faces(frame, confidence_threshold=0.5):
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177.0, 123.0))
    face_net.setInput(blob)
    output = np.squeeze(face_net.forward())
    faces = []
    for i in range(output.shape[0]):
        confidence = output[i, 2]
        if confidence > confidence_threshold:
            box = output[i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            start_x, start_y, end_x, end_y = box.astype(np.int_)
            start_x, start_y, end_x, end_y = start_x - \
                10, start_y - 10, end_x + 10, end_y + 10
            start_x = max(start_x, 0)
            start_y = max(start_y, 0)
            end_x = max(end_x, 0)
            end_y = max(end_y, 0)
            faces.append((start_x, start_y, end_x, end_y))
    return faces

# Face Detection Function: Defines a function get_faces() which takes a frame (image) as input and detects faces within it. 
# It utilizes the pre-trained face detection model (face_net) to detect faces with a confidence threshold of 0.5.

# Processing Detected Faces: Extracts the bounding box coordinates for each detected face and adjusts them slightly for better visualization.
# These coordinates represent the region of interest (ROI) where faces are detected within the frame.

# Output: Returns a list of tuples containing coordinates of bounding boxes for each detected face within the input frame. 
# Each tuple represents the (start_x, start_y, end_x, end_y) coordinates of the bounding box surrounding a detected face.
