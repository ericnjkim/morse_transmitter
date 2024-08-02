## Morse Transmitter

### Project description:
This gui tool allows itself to be connected to another instance of the gui on
another machine with the use of the socket library, and uses morse to send
messages across this connection.


### Directory contents:
- bin: Executable files to run the gui tool.
- scripts: working files for the tool.
  - scripts/core: All logic for the working operation of the tool including use of the transcription model and any generic python library scripts.
  - scripts/qt: All qt related scripts for tying the core scripts into the gui's widgets.
  - scripts/run.py: Target point for the executable files to run the gui from.   


### Using the tool:
The gui upon execution requires a connection to be made to another instance of
the tool on another machine. This is done by getting the ip of the receiver
and inserting that into the gui's receiver_ip parameter and clicking connect.

Once connected, the buttons can be used to write in english with morse.

Dot and dash work as normal but since I haven't integrated a way for the buttons
to be timed and determine the end of a letter or a space from that, I added 
a slash button to signify the end of every letter and two slashes to signify a
space. The receiver should be receiving this message as it is typed out.

To clear the message, hit the clear button and it will clear on both your and
the receiver's message window.

### WIP
- Connect buttons to keyboard buttons as well. 
- See if I can get the morse buttons to be replaced with a single button and
work off timing for dots and dashes.