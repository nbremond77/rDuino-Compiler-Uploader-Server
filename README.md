## rDuino-Compiler-Uploader-Server##

Description
-----------
This small web server (a webapp), intented to run locally, that will receives a piece of Arduino code on port 5005, compile it and upload the binary to the target.
This server has been developed to close the gap between Blockly@rduino and the real Arduino target, when CodeBender.cc is not available or can not be used.

Install
-------
    sudo pip install Flask
    chmod +x rDuino_uploader_server.py

Usage
-----
Run the server on the local machine, using python, by entering the following commands in a terminal window.

    ./rDuino_uploader_server.py
or
    python rDuino_uploader_server.py

Leave the terminal open, so the server will run all the way along.


Design your application in Blockly@reduino.
Connect the Arduino target.
Go to the 127.0.0.1:5005 webpage and select the USB port on which your Arduino target is connected, and the appropriate Arduino board type.
Go back Blockly@reduino and click on the button:
        "Local upload in Arduino"

At this time, an HTTP request with the code is sent to 
http://127.0.0.1:5005/
along qith the code to be compiled.

The server get the code, prepare a shell command, and run it in order to have the code compiled, linked and uploaded to the target.

If no error is found, your code is uploaded in the Arduino target. 
You can get the results by looking at the page at
http://127.0.0.1:5005/
The bottom of this page is periodically refreshed.



Options
-------
rDuino_uploader_server can be run with the following options:

    $ ./rDuino_uploader_server.py  --help

    Usage: rDuino_uploader_server.py [options]

    Options:
      -h, --help            show this help message and exit
      -H HOST, --host=HOST  Hostname of the rDuino_Uploader_Server app [default :
                            127.0.0.1]
      -P PORT, --port=PORT  Ethernet port for the rDuino_Uploader_Server app
                            [default : 5005]
      -D DEVICE, --device=DEVICE
                            Address of the target to be programmed : ''[default :
                            ]
      -B BOARD, --board=BOARD
                            The type of board to be programmed :
                            'arduino:avr:uno',
                            'arduino:avr:mega:cpu=atmega2560'[default :
                            arduino:avr:uno]
      -O OPTION, --option=OPTION
                            Options to be used for programming and uploading the
                            code : '', '--verbose-upload', '--verbose-build', '--
                            verbose', '--preserve-temp-files'[default : ]
      -T TOOL_PATH, --tool-path=TOOL_PATH
                            path of the Arduino tools : [default :
                            D:\Users\s551544\Personnel\Tools\Arduino\]
      -U UPLOAD_EXEC, --upload-exec=UPLOAD_EXEC
                            exec to be launched to compile and program the target
                            : [default : arduino.exe]
      -C COMPILE_EXEC, --compile-exec=COMPILE_EXEC
                            exec to be launched to open the Arduino IDE : [default
                            : arduino.exe]

example:

    ./rDuino_uploader_server.py -D /dev/ttyUSB3 -P 5555 -B arduino:avr:mega -O --verbose-upload

