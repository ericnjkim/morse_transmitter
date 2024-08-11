## Morse Transmitter

### Project description:
This gui tool allows itself to be connected to another instance of the gui on
another machine with the use of the socket library, and uses morse to send
messages across this connection.

<img src="/_readme_images/morse_transmitter_gui.png" alt="morse_transmitter_gui" width="700"/>

### Directory contents:
Further docstrings can be found in modules.

- executables/: Compiled standalone exe to run the project and spec file to build
the exe.
- scripts/: working files for the tool.
  - scripts/core/: All logic for the working operation of the tool including use of the transcription model and any generic python library scripts.
  - scripts/qt/: All qt related scripts for tying the core scripts into the gui's widgets.
    - scripts/qt/qss/: Qt style sheet and icons for the gui.
    - scripts/qt/ui/: The ui files for the widget layout of the gui.

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

### Credits
Qss style sheet base before modifications and qss icons: 
https://github.com/SZinedine/QBreeze

### WIP
- See if I can get the morse buttons to be replaced with a single button and
work off timing for dots and dashes.