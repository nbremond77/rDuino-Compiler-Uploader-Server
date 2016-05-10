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
myCompileAndUploadOption = "-upload"
myTarget = "/dev/ttyUSB0"
myTempDirectory = "/tmp/"

app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello World!'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      theCode = "??"
      f = request.files['the_file']
      f.save(myTempDirectory + 'uploaded_file.txt')
        
    return render_template('main.html', code=theCode)
        
if __name__ == '__main__':
    app.run(port=myPort)
