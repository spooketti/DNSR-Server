from flask import Flask, request, jsonify, make_response, Response
from init import app
from init import cors
import io
from imageio import imread
import base64
from ageWithGender import predict_age_and_gender
import numpy as np
import cv2


@app.route('/')
def home():
    return "Physiognomy's Server"
  
@app.route("/getPrediction/",methods=["POST"])
def getPrediction():
  data = request.get_json() 
  b64img = data["image"].split(",")[1]
  imgdat = base64.b64decode(b64img)
  image_array = np.frombuffer(imgdat, dtype=np.uint8)
  #opencv_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
  
  result = predict_age_and_gender(image_array)
  return jsonify({'image': result})

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://172.27.233.236:3000', 'https://spooketti.github.io']:
        cors._origins = allowed_origin

def run():
  app.run(host='0.0.0.0',port=6221)
#predict_age_and_gender("brick.jpg")
run()
