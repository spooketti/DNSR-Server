import cv2
from face import get_faces
from init import MODEL_MEAN_VALUES, age_net, AGE_POINTS, frame_width, gender_net, GENDER_LIST, GENDER_DICT

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))
    # resize the image
    return cv2.resize(image, dim, interpolation = inter)

def predict_age_and_gender(input_path: str):
    """Predict the age of the faces showing in the image"""
    # Read Input Image
    img = cv2.imread(input_path)
    # Take a copy of the initial image and resize it
    frame = img.copy()
    if frame.shape[1] > frame_width:
        frame = image_resize(frame, width=frame_width)
    faces = get_faces(frame)
    if(len(faces) < 1):
        return "No Faces Found!"
    for i, (start_x, start_y, end_x, end_y) in enumerate(faces):
        face_img = frame[start_y: end_y, start_x: end_x]
        
        # image --> Input image to preprocess before passing it through our dnn for classification.
        blob = cv2.dnn.blobFromImage(
            image=face_img, scalefactor=1.0, size=(227, 227), 
            mean=MODEL_MEAN_VALUES, swapRB=False
        )
        #gender
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()
        i = gender_preds[0].argmax()
        gender = GENDER_LIST[i]
        gender_confidence_score = gender_preds[0][i]
            
        #age
        age_net.setInput(blob)
        age_preds = age_net.forward()
        print("="*30, f"Face {i+1} Prediction Probabilities", "="*30)
        for i in range(age_preds[0].shape[0]):
            print(f"{AGE_POINTS[i]}: {age_preds[0, i]*100:.2f}%")
        i = age_preds[0].argmax()
        age = AGE_POINTS[i]
        age_confidence_score = age_preds[0][i]
        # Draw the box
        if(gender_confidence_score > .5):
            cv2.putText(frame,f"{gender} - {age_confidence_score * 100:.2f}%",(start_x,end_y),cv2.FONT_HERSHEY_SIMPLEX, 1, GENDER_DICT[gender], 2)
        label = f"Age:{age} - {age_confidence_score*100:.2f}%"
        print(label)
        # get the position where to put the text
        yPos = start_y - 15
        while yPos < 15:
            yPos += 15
        # write the text into the frame
        cv2.putText(frame, label, (start_x, yPos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), thickness=2)
        # draw the rectangle around the face
        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), color=(255, 0, 0), thickness=2)
    # Display processed image
    # Display Image on screen
        cv2.imshow("Temp", frame)
    # Mantain output until user presses a key
        cv2.waitKey(0)
    # Destroy windows when user presses a key
        cv2.destroyAllWindows()
    # save the image if you want
    # cv2.imwrite("predicted_age.jpg", frame)