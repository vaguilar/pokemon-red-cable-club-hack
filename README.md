Pokemon Red Cable Club Hack
===========================

[https://www.youtube.com/watch?v=m3e_SyhE3xc](https://www.youtube.com/watch?v=m3e_SyhE3xc)

This is a proof of concept to demonstrate a buffer overflow in the Cable Club. This project contains the assembly and binary data that is sent to the Gameboy along with two ways to send it.

## Arduino
Cut open a link cable open and wire it to the Arduino like so:

     ___________
    |  6  4  2  |
     \_5__3__1_/   (at cable)

    Cable Pin   Name           Arduino Pin
       1        VCC                N/A
       2        Serial Out         6
       3        Serial In          3
       4        Serial Data        N/A
       5        Serial Clock       2
       6        GND                GND

Upload the program inside the arduino folder and run Pokemon red. Visit the Cable Club and proceed to the Trade Center where the program will execute.

## BGB Emulator Link
Start the emulator with Pokemon Red. Right click on the emulator window and select Link > Listen. Then run the python script, with an optional port to connect to (default is 8765).

./bgb_link.py [port]

## Building Your Own Program
* Copy a directory like the hello project in the asm folder
* Edit the build and linkfile to match the name of your project (change "hello" to whatever you are naming your files)
* Then go to the py directory, edit the cable_club.py to open your bin file instead.
* If running on the Arduino, run cable\_club.py (python cable\_club.py) and copy the new DATA_BLOCK array line (replacing the old one) to the pokemonspoof.h file in the arduino folder. Upload to the Arduino and run.
