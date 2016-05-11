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
boardList = [ "arduino:avr:uno",  "arduino:avr:mega"]
#myBoard = "arduino:avr:nano:cpu=atmega168"
#myBoard = "arduino:avr:mega"
myBoard = "arduino:avr:uno"

myTargetOption = "--port"
#targetList = ["COM1","COM2","COM3","COM4","COM5","COM6"]
targetList = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3", "/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3"]
#myTarget = "COM3"
myTarget = "/dev/ttyUSB0"
#myTarget = "/dev/ttyACM0"

myOtherOptions = ""

#separator = "\"  # Windows
separator = "/"  # Linux
myTempDirectory = "/tmp/uploaded_file"

myCmd = ""
theResult = ""


# Define the main application
app = Flask(__name__)

# Define the routes

# Install a new library in the Arduino IDE
@app.route('/install_library', methods=['GET', 'POST'])
def install_library():
     # arduino --install-library "Bridge:1.0.0"
    if request.method == 'POST':
        myCmd = ""
        theResult = ""
        theLibrary = request.form['library']
        myCmd = myArduinoExe+" "+myInstallLibrary+" "+theLibrary
        print("%s ..." % myCmd)
        #theResult = os.system(myCmd)
        print(" Done. Result:%s\n" % theResult)
    return render_template('install_library.html', cmd=myCmd, result=theResult)


# Install a new baord in the Arduino IDE
@app.route('/install_boards', methods=['GET', 'POST'])
def install_boards():
     # arduino --install-boards "arduino:sam"
    if request.method == 'POST':
        myCmd = ""
        theResult = ""
        theBoard = request.form['board']
        myCmd = myArduinoExe+" "+myInstallBoard+" "+theBoard
        print("%s ..." % myCmd)
        #theResult = os.system(myCmd)
        print(" Done. Result:%s\n" % theResult)
    return render_template('install_boards.html',  theBoardList=boardList, cmd=myCmd, result=theResult)

# Define the target address
@app.route('/set_target', methods=['GET', 'POST'])
def set_target():
    if request.method == 'POST':
        myTarget = request.form['taget']
        print("Taget set to:%s\n" % myTarget)
    return redirect('/')
    
# Define the board
@app.route('/set_board', methods=['GET', 'POST'])
def set_board():
    if request.method == 'POST':
        myBoard = request.form['board']
        print("Board set to:%s\n" % myBoard)
    return redirect('/')
    
# Main page, and process code compile and upload requests
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        theResult = ""
        theCode = ""
        myCmd = ""
        myFileName = 'uploaded_file.ino'
        
        tmp = request.data
        theCode = tmp.decode(encoding='UTF-8')
        print("\nThe code:\n%s\n" % theCode)
        
        # Write the code to a temp file
        with open(myTempDirectory + separator + myFileName, "w") as f:
            f.write("%s" % theCode)
    
        myCmd = myArduinoExe+" "+myBoardOptions+" "+myBoard+" "+myTargetOption+" "+myTarget+" "+myOtherOptions+" "+myCompileAndUploadOption+" "+myTempDirectory+separator+myFileName
        print("\nThe shell command:\n%s\n" % myCmd)

        theResult = os.system(myCmd)
        print("\nThe output of the compiler-linker-uploader:\n%s\n" % theResult)
        print(" Done.\n")
        
        return theResult
    
    return render_template('main.html', thePort=myPort, theBoardList=boardList, theBoard=myBoard, theTargetList=targetList, theTarget=myTarget, theTempFile=myTempDirectory+separator+myFileName, result=theResult)

if __name__ == '__main__':

    # Create the temp file directory if needed
    if not(os.path.isdir(myTempDirectory)):
        os.system("mkdir "+myTempDirectory)
        
    # Start the main server
    app.run(port=myPort)
