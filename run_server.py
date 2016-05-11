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
import subprocess

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
targetList = ["ttyUSB0", "ttyUSB1", "ttyUSB2", "ttyUSB3", "ttyACM0", "ttyACM1", "ttyACM2", "ttyACM3"]
#myTarget = "COM3"
myTargetRoot="/dev/"
myTarget = "ttyUSB0"
#myTarget = "ttyACM0"

#myOtherOptions = "--verbose-upload"
myOptionList = ["", "--verbose-upload",  "--verbose-build",  "--verbose",  "--preserve-temp-files"]
myOption = ""

#separator = "\"  # Windows
separator = "/"  # Linux
myTempDirectory = "/tmp/uploaded_file"

myCmd = ""
theResult = ""
theError = ""
myFileName = "uploaded_file.ino"


# Define the main application
app = Flask(__name__)

# Define the routes

# Install a new library in the Arduino IDE
@app.route('/install_library', methods=['GET', 'POST'])
def install_library():
    global theResult
    global theError
    global myCmd

    if request.method == 'POST':
        myCmd = ""
        theResult = ""
        theError  =""
        theLibrary = request.form['library']
        # arduino --install-library "Bridge:1.0.0"
        myCmd = myArduinoExe+" "+myInstallLibrary+" "+theLibrary
        print("%s ..." % myCmd)
        #theResult = os.system(myCmd)
        proc = subprocess.Popen(myCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        result = out.decode(encoding='UTF-8')
        theResult = result.replace("\n","<br/>")
        error = err.decode(encoding='UTF-8')
        theError = error.replace("\n","<br/>")
        
        print(" Done. Result:%s\n" % result)
    return render_template('install_library.html', cmd=myCmd, result=theResult, error=theError)


# Install a new baord in the Arduino IDE
@app.route('/install_board', methods=['GET', 'POST'])
def install_board():
    global theResult
    global theError
    global myCmd

    if request.method == 'POST':
        myCmd = ""
        theResult = ""
        theError = ""
        theBoard = request.form['board']
        # arduino --install-boards "arduino:sam"
        myCmd = myArduinoExe+" "+myInstallBoard+" "+theBoard
        print("%s ..." % myCmd)
#        theResult = os.system(myCmd)
        proc = subprocess.Popen(myCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        result = out.decode(encoding='UTF-8')
        theResult = result.replace("\n","<br/>")
        error = err.decode(encoding='UTF-8')
        theError = error.replace("\n","<br/>")
        
        print(" Done. Result:%s\n" % result)
    return render_template('install_board.html',  theBoardList=boardList, theBoard=myBoard, cmd=myCmd, result=theResult, error=theError)

# Define the target address
@app.route('/set_target', methods=['GET', 'POST'])
def set_target():
    global myTarget
    if request.method == 'POST':
        myTarget = request.form['target']
        print("Taget set to:[%s]\n" % (myTargetRoot + myTarget))
    return redirect('/')
    
# Define the board
@app.route('/set_board', methods=['GET', 'POST'])
def set_board():
    global myBoard
    if request.method == 'POST':
        myBoard = request.form['board']
        print("Board set to:[%s]\n" % myBoard)
    return redirect('/')
    
# Define the board
@app.route('/set_option', methods=['GET', 'POST'])
def set_option():
    global myOption
    if request.method == 'POST':
        myOption = request.form['option']
        print("Option set to:[%s]\n" % myOption)
    return redirect('/')
    
# Main page, and process code compile and upload requests
@app.route('/', methods=['GET', 'POST'])
def main_page():
    global theResult
    global theError
    global myCmd
    global myFileName
    
    if request.method == 'POST':

        theResult = ""
        theError = ""
        theCode = ""
        myCmd = ""
        myFileName = 'uploaded_file.ino'
        
        tmp = request.data
        theCode = tmp.decode(encoding='UTF-8')
        print("\nThe code:\n%s\n" % theCode)
        
        # Write the code to a temp file
        with open(myTempDirectory + separator + myFileName, "w") as f:
            f.write("%s" % theCode)
    
        # arduino --board arduino:avr:nano:cpu=atmega168 --port /dev/ttyACM0 --upload /path/to/sketch/sketch.ino
        myCmd = myArduinoExe+" "+myBoardOptions+" "+myBoard+" "+myTargetOption+" "+myTargetRoot+myTarget+" "+myOption+" "+myCompileAndUploadOption+" "+myTempDirectory+separator+myFileName
        print("\nThe shell command:\n%s\n" % myCmd)

#        theResult = os.system(myCmd)
        proc = subprocess.Popen(myCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        result = out.decode(encoding='UTF-8')
        theResult = result.replace("\n","<br/>")
        error = err.decode(encoding='UTF-8')
        theError = error.replace("\n","<br/>")
        
        print("\nThe output of the compiler-linker-uploader:\n%s\n" % result)
        print("\nThe errors :\n%s\n" % error)
        print(" Done.\n")
        
#        return result
#        return redirect('/')        
    
    return render_template('main.html', thePort=myPort, theBoardList=boardList, theBoard=myBoard, theTargetList=targetList, theTarget=myTarget, theOptionList=myOptionList, theOption=myOption, theTempFile=myTempDirectory+separator+myFileName, result=theResult, error=theError)

if __name__ == '__main__':

    # Create the temp file directory if needed
    if not(os.path.isdir(myTempDirectory)):
        os.system("mkdir "+myTempDirectory)
        
    # Start the main server
    app.run(port=myPort)
