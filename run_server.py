#!/usr/bin/env python
# -*- coding: utf-8 -*-


# --------------------------------------------------------------------
# rDuino-Compiler-Uploader-Server : Mini server to compile and upload
# a code to the target board.
#
# This program serves HTTP requests on port 888
# Compile and upload the code using the arduino IDE (linux)
#
# --------------------------------------------------------------------

 # from http://flask.pocoo.org/ 
from flask import Flask

# Configuration data
myPort = 888
myArduinoExe = "arduino"
myCompileAndUploadOption= "-upload"
myTempDirectory = "/tmp"

app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello World!'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/tmp/uploaded_file.txt')
        
    return 'Hello World!'
        
if __name__ == '__main__':
    app.run(port=myPort)
