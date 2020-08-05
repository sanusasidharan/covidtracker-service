from flask import Flask, jsonify, request, send_file , send_from_directory
import os
import socket

# creating a Flask app 
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"
	
	
PORT = int(os.getenv('PORT', 8000))
# Change current directory to avoid exposure of control files
#os.chdir('/static')
host_name = socket.gethostname() 
host_ip = socket.gethostbyname(host_name)
        
# driver function 
if __name__ == '__main__': 
    app.run(debug = True , host=host_ip, port=PORT )