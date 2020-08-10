from flask import Flask, jsonify, request, send_file , send_from_directory
import sys
import cv2
import os
from sys import platform
import numpy as np
import socket
from werkzeug.utils import secure_filename
import json
import uuid
from datetime import datetime
import time
import array
from datetime import datetime
import csv
import io
# creating a Flask app
app = Flask(__name__)
classifier = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
loc = os.environ.get('DATA_PATH','D:/TestData/')
cropped = loc+"/cropped/"


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/api/crop', methods=['POST'])
def crop():
    content = request.json
    fileName=cropFile(loc+content['filename'])

    return fileName

def cropFile(image):
    print('image:',image )
    image_copy = cv2.imread(image)
    gray_image = cv2.cvtColor(image_copy, cv2.COLOR_RGB2GRAY)
    faces = classifier.detectMultiScale(gray_image, 1.25, 6)
    print('Number of faces detected:', len(faces))
    if(len(faces)!=0):
       face_crop = []
       for f in faces:
         x, y, w, h = [ v for v in f ]
         cv2.rectangle(image_copy, (x,y), (x+w, y+h), (255,0,0), 3)
         face_crop.append(gray_image[y:y+h, x:x+w])
    #facelen = 0
       for face in face_crop:
         croppedFileName = '{}{:-%Y%m%d%H%M%S}.jpg'.format(str(uuid.uuid4().hex), datetime.now())
         cv2.imwrite(cropped+croppedFileName,face)
         return croppedFileName
    else:
        croppedFileName= ''
        return  croppedFileName

# route http posts to this method
@app.route('/api/temp', methods=['POST'])
def calculateTemperature():
    content = request.json
    filename=content['filename']
    tmp,avg = tempCalculator(cropped+filename)
    data_set = {"temperature": tmp, "average": avg}
    json_dump = json.dumps(data_set)
    print(json_dump)
    #jsonObj = jsonify(temprature=tmp,average=avg)
    #jsonObj = jsonify({temperature=tmp,average=avg})
    return json_dump

def tempCalculator(inputImageToProcess):
    try:
        imageToProcess = cv2.imread(inputImageToProcess)
        print('temp calc hit')
        if imageToProcess is None:
            print('imageToProcess is none')
        try:
            h, w, c = imageToProcess.shape
        except:
            h,w,c = 200,400,40
        #processing
        gray = cv2.cvtColor(imageToProcess, cv2.COLOR_BGR2GRAY)
        gray_inverted = cv2.bitwise_not(gray)
        imageToProcess = cv2.cvtColor(gray_inverted, cv2.COLOR_GRAY2BGR)
        size_x = int(h)-10
        size_y = int(w)-10
        minVal = size_x < size_y and size_x or size_y
        size_x,size_y = minVal,minVal
        reference_x = 0
        reference_y = 0
        offset_x = 0
        offset_y = 0
        average = 0
        counter = 0

        # Calculate average values in face rect
        for y in range(reference_x-size_x+offset_x, reference_x+size_x+offset_x):
            for x in range(reference_y-size_y+offset_y, reference_y+size_y+offset_y):
                average += imageToProcess[x, y][0]
                counter += 1
        #Calculate average
        if counter!=0:
            average = average / counter
        #Print data
        if counter!=0:
            # Get pixel value of reference point
            reference_temperature = imageToProcess[size_x, size_y][0];

            #Temperature calculation with reference point temperature
            temperature = (average * float(45))/reference_temperature

            #Print some data about temperature
            print("Face rect temperature: T:{0:.2f}C, {1:.2f}".format(temperature, average))

            return temperature,average

    except Exception as e:
        print(e)


PORT = int(os.getenv('PORT', 3000))
# Change current directory to avoid exposure of control files
#os.chdir('/static')
host_name = socket.gethostname() 
host_ip = socket.gethostbyname(host_name)
        
# driver function 
if __name__ == '__main__': 
    app.run(debug = True , host=host_name, port=PORT )