## Morse Transmitter

### Project description:
This gui tool allows itself to be connected to another instance of the gui on
another machine with the use of the socket library, and uses morse to send
messages across this connection.

<img src="/_readme_images/morse_transmitter_gui.png" alt="morse_transmitter_gui" width="700"/>

### Directory contents:
Further docstrings can be found in modules.

- scripts/: working files for the tool.
    - scripts/qss/: Qt style sheet and icons for the gui.
    - scripts/ui/: The ui files for the widget layout of the gui.

### Installation and running:
This project used python3.12 and can be run directly in an editor or through 
a terminal by running `python scripts/morse_transmitter_main.py` within a venv.

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

### How it works:

#### Morse clicker:
Uses buttons for `. _ /` to write out a morse letter. 
The `/` allows the user to state when we've reached the end of 
a letter and two of these will create a space.
The `/` is not part of morse but because the gui uses buttons rather than a 
timer to dictate what is a dot and dash, we also needed a way to determine the
end of a letter or word without a timer.

#### Socket operations:
Each instance of the gui has a server thread and client thread. 
The server is used as the communication line between two gui's through their
client threads and the client threads are what send and receive data and decide 
how to handle received data in the main gui by emitting custom signals.

When the gui is hosting, the server will activate and the client will connect to 
the local server. This will then allow one other gui to connect to this server 
and upon this successful connection, the communication between these two gui's 
will be live.

When the gui is connecting to a host, the server thread is kept deactivated and 
the client thread will attempt to connect to the target host.

<img src="/_readme_images/server_client_diagram.png" alt="server_client_diagram" width="700"/>

#### Displaying received data on the gui:
The client thread acts as a handler for incoming data. When a message is 
received, it emits a signal to the main gui that displays the message on 
the received message text box. Special action messages such as /clear and 
/status_log:message are handled as separate actions so upon receiving these,
the client thread will emit other signals for clearing the received message box
and to display a message in the status log.

I usually prefer to keep logic separate to the qt scripts but in this case
I had to integrate the two as I needed a way for a receiver function to 
continuously receive a message and act upon it without ending the loop 
with a return function which I was able to do by having the receiver 
simultaneously emit signals upon receiving new messages.

### Challenges:
Socket operations: This is the first project I had to use sockets and a network to have a 
communicative path between two guis so it took a while of trial and error to
come to a solution of how to get a gui to be both capable of hosting or 
connecting.

Debugging: The use of multiple Qthreads as part of the socket made debugging and 
backtracking where things were going wrong quite difficult so logging from the 
logging library was integrated to provide a more robust way to track all actions
and events each gui had.

### Credits
Qss style sheet base before modifications and qss icons: 
https://github.com/SZinedine/QBreeze

### WIP
- See if I can get the morse buttons to be replaced with a single button and
work off timing for dots and dashes.
- Disconnect operations for sockets need to be fixed and integrated.
- Compile project into executable file.
- Get qss working.