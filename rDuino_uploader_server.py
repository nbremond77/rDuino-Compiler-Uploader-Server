#!/usr/bin/env python
# -*- coding: utf-8 -*-


# --------------------------------------------------------------------
# rDuino_Uploader_Server : Mini server to compile and upload
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
import sys
import glob
import serial
import subprocess
from datetime import datetime
import optparse

# from http://flask.pocoo.org/ 
from flask import Flask, abort, redirect, url_for, request, render_template,  Markup,  make_response,  session,  escape,  jsonify

# Configuration data
#debugMode = 0

myPort = 5005


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

#myOtherOptions = "--verbose-upload"
myOptionList = ["", "--verbose-upload",  "--verbose-build",  "--verbose",  "--preserve-temp-files"]
myOption = ""

if sys.platform.startswith('win'):
    separator = "\\"  # Windows
    myTempDirectory = "\\$HOME"
    myArduinoExe = "arduino_debug.exe" # Windows
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    # this excludes your current terminal "/dev/tty"
    separator = "/"  # Linux
    myTempDirectory = "/tmp/uploaded_file"
    myArduinoExe = "export DISPLAY=:0.0 && arduino " # Linux
elif sys.platform.startswith('darwin'):
    separator = "/"  # Mac - Not tested
    myTempDirectory = "/tmp/uploaded_file"
    myArduinoExe = "Arduino.app/Contents/MacOS/Arduino" # MAC - not tested
else:
    raise EnvironmentError('Unsupported platform')


myCmd = ""
theResult = ""
theError = ""
theReturnCode = 0
compileTime = datetime.now()
myFileName = "uploaded_file.ino"

myProc = None

    
# Define the main application
app = Flask(__name__)





# This function return a list of the available serial ports. Works on any system
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
    

#targetList = ["COM1","COM2","COM3","COM4","COM5","COM6"]
#targetList = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3", "/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3"]
targetList = serial_ports()
#myTarget = "COM3"
myTarget = "/dev/ttyUSB0"
#myTarget = "/dev/ttyACM0"
#myTarget = targetList[1]

    
#global app

# Define the routes

# Install a new library in the Arduino IDE
@app.route('/install_library', methods=['GET', 'POST'])
def install_library():
    global theResult
    global theError
    global theReturnCode
    global myCmd

    if request.method == 'POST':
        myCmd = ""
        theResult = ""
        theError  =""
        theReturnCode = 0        
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
    global theReturnCode
    global myCmd

    if request.method == 'POST':
        myCmd = ""
        theResult = ""
        theError = ""
        theReturnCode = 0        
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
    global theResult
    global theError
    global theReturnCode

    if request.method == 'POST':
        myTarget = request.form['target']
        print("Taget set to:[%s]\n" % (myTarget))
        theResult = ""
        theError = ""
        theReturnCode = 0        
    return redirect('/')
    
# Define the board
@app.route('/set_board', methods=['GET', 'POST'])
def set_board():
    global myBoard
    global theResult
    global theError
    global theReturnCode

    if request.method == 'POST':
        myBoard = request.form['board']
        print("Board set to:[%s]\n" % myBoard)
        theResult = ""
        theError = ""
        theReturnCode = 0        
    return redirect('/')
    
# Define the board
@app.route('/set_option', methods=['GET', 'POST'])
def set_option():
    global myOption
    global theResult
    global theError
    global theReturnCode

    if request.method == 'POST':
        myOption = request.form['option']
        print("Option set to:[%s]\n" % myOption)
        theResult = ""
        theError = ""
        theReturnCode = 0        
    return redirect('/')

@app.route('/get_result')
def get_result():
    global theResult
    global compileTime
    global theReturnCode
    global myProc
    
    if myProc:
        for line in myProc.stdout:
            #out = str(line.rstrip())
            result = line.decode('utf-8')
            theResult = theResult + result.replace("\n","<br/>")
            print("   ++ Result:[%s]\n" % result)
        #myProc.stdout.flush()
       
    theTime = datetime.now()
#    print("result: %s\n" % theTime.strftime("%A %d %B %Y %H:%M:%S") + theResult)
#    print("compile time : %s\n" % compileTime.strftime("%A %d %B %Y %H:%M:%S"))
    return jsonify(date=theTime.strftime("%A %d %B %Y %H:%M:%S"),  compileTime =  compileTime.strftime("%A %d %B %Y %H:%M:%S"), result=theResult,   returnCode=theReturnCode)
#    return time.strftime("%A %d %B %Y %H:%M:%S") + theResult

@app.route('/get_error')
def get_error():
    global theError
    global myProc
    global theReturnCode

    if myProc:
        for line in myProc.stderr:
            #err = str(line.rstrip())
            error = line.decode('utf-8')
            theError = theError + error.replace("\n","<br/>")
            print("   ++ Error:[%s]\n" % error)
        #myProc.stderr.flush()    

        status = myProc.poll()
        if status is not None: # End of subprocess
            if (theError.find("can't open") >= 0):
                theReturnCode = -2 # Error
            elif (theError.find("stk500_getsync") >= 0):
                theReturnCode = -2 # Error
            else:
                theReturnCode = 2 # Good
            
    return jsonify(error = theError,  returnCode=theReturnCode)
#    return theError


# Open the code in the Arduino IDE
@app.route('/openIDE', methods=['GET', 'POST'])
def openIDE():
    global theResult
    global theError
    global theReturnCode
    global myCmd
    global myFileName
    global compileTime
    global myProc
    
    if request.method == 'POST':

        theResult = ""
        theError = ""
        theReturnCode = 0
        theCode = ""
        myCmd = ""
        myFileName = "uploaded_file.ino"
        
#        tmp = request.data
        theCode = tmp.decode(encoding='UTF-8')
        theCode = tmp
        theFileName = myTempDirectory + separator + myFileName
        print("The code:\n%s\n" % theCode)
        print("Try to save the code to a local file %s\n" % theFileName)

        # Write the code to a temp file
        try:
            f = open(theFileName, "w")
            print("Trying...\n")
#        except (OSError, IOError) as err:
        except:
            print("Unable to open file for writing: IOError: %s\n" % sys.exc_info()[0])
        else:
            try:
                print("Writing...\n")
                f.write(theCode)
                print("Code written to %s\n" % theFileName)
#            except  (OSError, IOError) as err:
            except:
                print("Unable to write in the file : %s\n" % sys.exc_info()[0])
            finally:
                f.close()
                print("File closed.\n")


        # arduino --board arduino:avr:nano:cpu=atmega168 --port /dev/ttyACM0 --upload /path/to/sketch/sketch.ino
        compileTime = datetime.now()
        myCmd = myArduinoExe+" "+myBoardOptions+" "+myBoard+" "+myTargetOption+" "+myTarget+" "+myOption+" "+myTempDirectory+separator+myFileName
        print("\nThe shell command:\n%s\n" % myCmd)

#        theResult = os.system(myCmd)
        myProc = subprocess.Popen(myCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#        myProc = subprocess.Popen(myCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Subprocess blocking
        #(out, err) = myProc.communicate()
        
        # Non blocking
        theResult = myCmd + "<br/><br/>"
            
        if myProc:
            for line in myProc.stdout:
                #out = str(line.rstrip())
                result = line.decode('utf-8')
                theResult = theResult + result.replace("\n","<br/>")
            print("-- Result:[%s]\n" % theResult)
            #myProc.stdout.flush()
            for line in myProc.stderr:
                #err = str(line.rstrip())
                error = line.decode('utf-8')
                theError = theError + error.replace("\n","<br/>")
            print("-- Error:[%s]\n" % theError)
            #myProc.stderr.flush()  
            
#        result = out.decode(encoding='UTF-8')
#        theResult = result.replace("\n","<br/>")
#        error = err.decode(encoding='UTF-8')
#        theError = error.replace("\n","<br/>")

        print("\nThe output of the compiler-linker-uploader:\n%s\n" % theError)
        print("\nThe errors :\n%s\n" % theError)
        print("\nThe Return Code :\n%s\n" % theReturnCode)
        print(" Done.\n")
    
    return render_template('main.html', thePort=myPort, theBoardList=boardList, theBoard=myBoard, theTargetList=targetList, theTarget=myTarget, theOptionList=myOptionList, theOption=myOption, theTempFile=myTempDirectory+separator+myFileName, result=theResult, error=theError)


    
# Main page, and process code compile and upload requests
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global theResult
    global theError
    global theReturnCode
    global myCmd
    global myFileName
    global compileTime
    global myProc
    
    if request.method == 'POST':

        theResult = ""
        theError = ""
        theReturnCode = 0
        theCode = ""
        myCmd = ""
        myFileName = "uploaded_file.ino"
        
        tmp = request.data
        theCode = tmp.decode(encoding='UTF-8')
#        theCode = tmp
        theFileName = myTempDirectory + separator + myFileName
        print("The code:\n%s\n" % theCode)
        print("Try to save the code to a local file %s\n" % theFileName)

        # Write the code to a temp file
        try:
            f = open(theFileName, "w")
            print("Trying...\n")
#        except (OSError, IOError) as err:
        except:
            print("Unable to open file for writing: Error: %s\n" % sys.exc_info()[0])
        else:
            try:
                print("Writing...\n")
                f.write(theCode)
                print("Code written to %s\n" % theFileName)
#            except  (OSError, IOError) as err:
            except:
                print("Unable to write in the file %s. Error : %s\n" % {theFileName,  sys.exc_info()[0]})
            finally:
                f.close()
                print("File closed.\n")


        # arduino --board arduino:avr:nano:cpu=atmega168 --port /dev/ttyACM0 --upload /path/to/sketch/sketch.ino
        compileTime = datetime.now()
        myCmd = myArduinoExe+" "+myBoardOptions+" "+myBoard+" "+myTargetOption+" "+myTarget+" "+myOption+" "+myCompileAndUploadOption+" "+myTempDirectory+separator+myFileName
        print("\nThe shell command:\n%s\n" % myCmd)

#        theResult = os.system(myCmd)
        myProc = subprocess.Popen(myCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#        myProc = subprocess.Popen(myCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Subprocess blocking
        #(out, err) = myProc.communicate()
        
        # Non blocking
        theResult = myCmd + "<br/><br/>"
            
        if myProc:
            for line in myProc.stdout:
                #out = str(line.rstrip())
                result = line.decode('utf-8')
                theResult = theResult + result.replace("\n","<br/>")
            print("-- Result:[%s]\n" % theResult)
            #myProc.stdout.flush()
            for line in myProc.stderr:
                #err = str(line.rstrip())
                error = line.decode('utf-8')
                theError = theError + error.replace("\n","<br/>")
            print("-- Error:[%s]\n" % theError)
            #myProc.stderr.flush()  
            
#        result = out.decode(encoding='UTF-8')
#        theResult = result.replace("\n","<br/>")
#        error = err.decode(encoding='UTF-8')
#        theError = error.replace("\n","<br/>")

        print("\nThe output of the compiler-linker-uploader:\n%s\n" % theError)
        print("\nThe errors :\n%s\n" % theError)
        print("\nThe Return Code :\n%s\n" % theReturnCode)
        print(" Done.\n")
    
    return render_template('main.html', thePort=myPort, theBoardList=boardList, theBoard=myBoard, theTargetList=targetList, theTarget=myTarget, theOptionList=myOptionList, theOption=myOption, theTempFile=myTempDirectory+separator+myFileName, result=theResult, error=theError)


# Main page, and process code compile and upload requests
@app.route('/', methods=['GET', 'POST'])
def main_page():
    global theResult
    global theError
    global theReturnCode
    global myCmd
    global myFileName
    global compileTime
    global myProc

    print(" Call main page.\n")
    
    return render_template('main.html', thePort=myPort, theBoardList=boardList, theBoard=myBoard, theTargetList=targetList, theTarget=myTarget, theOptionList=myOptionList, theOption=myOption, theTempFile=myTempDirectory+separator+myFileName, result=theResult, error=theError)

    
def flaskrun(app, default_host="127.0.0.1", 
                  default_port=myPort):
    """
    Takes a flask.Flask instance and runs it. Parses 
    command-line flags to configure the app.
    """
    global myTarget
    global targetList
    global myBoard
    global boardList
    global myOption    
    global myOptionList
    global myArduinoExe
    global debugMode

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the rDuino_Uploader_Server app " + \
                           "[default : %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Ethernet port for the rDuino_Uploader_Server app " + \
                           "[default : %s]" % default_port,
                      default=default_port)
    parser.add_option("-D", "--device",
                      help="Address of the target to be programmed : " + str(targetList).strip('[]')+ \
                           "[default : %s]" % myTarget,
                      default=myTarget)
    parser.add_option("-B", "--board",
                      help="The type of board to be programmed : " + str(boardList).strip('[]')+ \
                           "[default : %s]" % myBoard,
                      default=myBoard)
    parser.add_option("-O", "--option",
                      help="Options to be used for programming and uploading the code : " + str(myOptionList).strip('[]')+ \
                           "[default : %s]" % myOption,
                      default=myOption)
    parser.add_option("-E", "--exec",
                      help="path and exec to be launched to compile and program the target : " + \
                           "[default : %s]" % myArduinoExe,
                      default=myArduinoExe)
    #parser.add_option("-d", "--debug",
    #                  help="Debug mode of Falsk. Do not use in production... : " + \
    #                       "[default : %s]" % debugMode,
    #                  default=debugMode)

    # Two options useful for debugging purposes, but 
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--profile",
                      action="store_true", dest="profile",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()
    
    myTarget = options.device
    myBoard = options.board
    myOption = options.option
    myArduinoExe = options.exec

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                       restrictions=[30])
        options.debug = True

    print("\nRun the serveur with the following parameters :\n")
    print("   Host  : %s" % options.host)
    print("   Port  : %s" % options.port)
    print("   Device: %s" % myTarget)
    print("   Board : %s" % myBoard)
    print("   Option: %s" % myOption)
    print("   Exec  : %s" % myArduinoExe)

    #app.config['DEBUG'] = True
    
    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
    # Start the main server
    #app.run(port=myPort)    

if __name__ == '__main__':
    global app
    
    # Create the temp file directory if needed
    if not(os.path.isdir(myTempDirectory)):
        os.system("mkdir "+myTempDirectory)
    
    # Start the main server
    flaskrun(app)



