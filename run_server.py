#!/usr/bin/env python
# -*- coding: utf-8 -*-


# --------------------------------------------------------------------
# rDuino-Compiler-Uploader-Server : Mini server to compile and upload
# a code to the target board.
#
# This program serves HTTP requests on port 888
# Compile and upload the code using the arduino IDE (linux)
#
# Compile and upload example: arduino --board arduino:avr:nano:cpu=atmega168 --port /dev/ttyACM0 --upload /path/to/sketch/sketch.ino
# See here: https://github.com/arduino/Arduino/blob/ide-1.5.x/build/shared/manpage.adoc
#
# --------------------------------------------------------------------

import os

 # from http://flask.pocoo.org/ 
from flask import Flask, abort, redirect, url_for, request, render_template,  Markup,  make_response,  session,  escape

# Configuration data
myPort = 888
#myPort = 5000

#myArduinoExe = "arduino_debug.exe" # Windows
#myArduinoExe = "Arduino.app/Contents/MacOS/Arduino" # MAC
myArduinoExe = "arduino" # Linux

myCompileAndUploadOption = "--upload"
myVerify = "--verify"
myInstallLibrary = "--install-library"
myInstallBoard = "--install-boards"

myBoardOptions = "--board"
#myBoard = "arduino:avr:nano:cpu=atmega168"
#myBoard = "arduino:avr:mega"
myBoard = "arduino:avr:uno"

myTargetOption = "--port"
#myTarget = "COM3"
myTarget = "/dev/ttyUSB0"
#myTarget = "/dev/ttyACM0"

myOtherOptions = ""

#separator = "\"  # Windows
separator = "/"  # Linux
myTempDirectory = "/tmp/uploaded_file"

# Define the main application
app = Flask(__name__)

# Define the routes
@app.route('/install_library', methods=['GET', 'POST'])
def install_library():
    myCmd = ""
    theResult = ""
     # arduino --install-library "Bridge:1.0.0"
    if request.method == 'POST':
        theLibrary = request.form['library']
        myCmd = myArduinoExe+" "+myInstallLibrary+" "+theLibrary
        print("%s ..." % myCmd)
        #theResult = os.system(myCmd)
        print(" Done. Result:%s\n" % theResult)
    return render_template('install_library.html', cmd=myCmd, result=theResult)


@app.route('/install_boards', methods=['GET', 'POST'])
def install_boards():
    myCmd = ""
    theResult = ""
     # arduino --install-boards "arduino:sam"
    if request.method == 'POST':
        theBoard = request.form['board']
        myCmd = myArduinoExe+" "+myInstallBoard+" "+theBoard
        print("%s ..." % myCmd)
        #theResult = os.system(myCmd)
        print(" Done. Result:%s\n" % theResult)
    return render_template('install_boards.html', cmd=myCmd, result=theResult)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    theResult = ""
    theCode = "??"
    myCmd = ""
    if request.method == 'POST':
        myFileName = 'uploaded_file.ino'
        
        tmp = request.data
        theCode = tmp.decode(encoding='UTF-8')

        
        with open(myTempDirectory + separator + myFileName, "w") as f:
            f.write("%s" % theCode)
    
        print("%s\n" % theCode)
     
        myCmd = myArduinoExe+" "+myBoardOptions+" "+myBoard+" "+myTargetOption+" "+myTarget+" "+myOtherOptions+" "+myCompileAndUploadOption+" "+myTempDirectory+separator+myFileName
        print("%s\n" % myCmd)
        theResult = os.system(myCmd)
        print("%s\n" % theResult)
        print(" Done.\n")
    
    return render_template('main.html', code=theCode, result=theResult, cmd=myCmd)
#    return render_template('main.html')
#    return "hello"

# Start the main server
if __name__ == '__main__':

    if not(os.path.isdir(myTempDirectory)):
        os.system("mkdir "+myTempDirectory)
        
    app.run(port=myPort)
