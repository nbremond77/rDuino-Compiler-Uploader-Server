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

 # from http://flask.pocoo.org/ 
from flask import Flask

# Configuration data
myPort = 888

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
#myTarget = "/dev/ttyUSB0"
myTarget = "/dev/ttyACM0"

myOtherOptions = ""

myTempDirectory = "/tmp/"


app = Flask(__name__)

@app.route('/install_library')
def install_library():
     # arduino --install-library "Bridge:1.0.0,Servo:1.2.0"
      theLibrary = "??"
      cmd = myArduinoExe+" "+myInstallLibrary+" "+theLibrary
      print("%s ..." % cmd)
      #theResult = exec(cmd)
      print(" Done.\n")
    return 'Done!'

#@app.route('/install_boards')
def install_boards():
     # arduino --install-boards "arduino:sam"
      theBoard = "??"
      cmd = myArduinoExe+" "+myInstallBoard+" "+theBoard
      print("%s ..." % cmd)
      #theResult = exec(cmd)
      print(" Done.\n")
    return 'Done!'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      theCode = "??"
      theResult = ""
      myFileName = 'uploaded_file.txt'
      f = request.files['the_file']
      f.save(myTempDirectory + myFileName)
      
      compileCmd = myArduinoExe+" "+myBoardOptions+" "+myBoard+" "+myTargetOption+" "+myTarget+" "+myOtherOptions+" "+myCompileAndUploadOption+" "+myTempDirectory+myFileName
      print("%s ..." % compileCmd)
      #theResult = exec(compileCmd)
      print(" Done.\n")
    
    return render_template('main.html', code=theCode, result=theResult)
        
if __name__ == '__main__':
    app.run(port=myPort)
