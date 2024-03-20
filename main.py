from flask import Flask, request, jsonify, make_response, Response
from init import app
from init import cors
from ageWithGender import predict_age_and_gender


@app.route('/')
def home():
    return "Physiognomy's Server"
  
@app.route("/getPrediction/",methods=["POST"])
def getPrediction():
  return "awsem"

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://172.27.233.236:3000', 'https://spooketti.github.io']:
        cors._origins = allowed_origin

def run():
  app.run(host='0.0.0.0',port=6221)
predict_age_and_gender("brick.jpg")
#run()
