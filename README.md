## rDuino-Compiler-Uploader-Server##

Description
-----------
This small web server, intented to run locally, receives pieces of Arduino code on port 888, compile it and upload the binary to the target.
This server has been developped to close the bridge between Blockly@rduino and the real Arduino target, when CodeBender.cc is not available, or can not be used.

Usage
-----
Run the server on the 
Server sur port 888
A exécuter en root
Qui va compiler et uploader le code vers la cible lorqu'on clique sur "Paste to arduino IDE" dans Blockly@rduino

Voici ce qui s'affiche lorsqu'on fait un test avec le code "blink":

    [nbremond@multimedia rDuino-Compiler-Uploader-Server]$ sudo ./run_server.py 
     * Running on http://127.0.0.1:888/ (Press CTRL+C to quit)
     
    void setup() {
      pinMode(13, OUTPUT);
    }
    
    void loop() {
      digitalWrite(13, HIGH);
      delay(100);
      digitalWrite(13, LOW);
      delay(300);
    
    }
    
    arduino --board arduino:avr:uno --port /dev/ttyUSB0  --upload /tmp/uploaded_file/uploaded_file.ino
    
    Picked up JAVA_TOOL_OPTIONS: 
    Loading configuration...
    Initialisation des paquets...
    Préparation des cartes
    Vérification et envoi...
    
    Le croquis utilise 1 066 octets (3%) de l'espace de stockage de programmes. Le maximum est de 32 256 octets.
    Les variables globales utilisent 9 octets (0%) de mémoire dynamique, ce qui laisse 2 039 octets pour les variables locales. Le maximum est de 2 048 octets.
    0
    
     Done.
    
    127.0.0.1 - - [10/May/2016 23:03:59] "POST / HTTP/1.1" 200 -



