# CS6250 Programming Assignment
-------------

Author     : Cheng Zhang

GTid        : 903433224

GT username   : czhang494

Affiliation     : Georgia Institute of Technology


## Description
-------------

The Trivial Twitter application uses TCP sockets to implement the application that allows users to publish their messages and also read other's messages.
In the tweet server program, the server will firstly get the port number from command line, then start to listen to the provided port on local machine and wait for connection request from the client(s).
In the client program, the client will first try to connection to the server by sending the connection request, if all requirements are satisfied, the server will then open a thread for this client to handle further commands and messages from this client, meanwhile the main thread will keep listening to new connection request from other client.
When connection established, the client will also create a new thread to listen to the data from the server, the data could be the ack from the server or the tweets from other clients, which also sent by the server. The main thread will collect messages from the client's stdin and send these messages to server.
After running the server, it will constantly maintain a dictionary of currently online clients and their socket objects, this will help to deny login request with duplicate username, as well as redirect tweets to client's mailbox. Each client will also maintain their own mailbox to temporarily store tweets from other clients.

## Folder Structure
-------------

├── ttweetsrc.py  # program to run the server 

├── ttweetcli.py   # program to run the client

├── Makefile 

├── sample_output.pdf   #sample output for section 2.3

└── README.md

## Running Program
-------------

Please run under the folder of this README.md

To start ttweet server:
    Run "python3 ttweetsrv.py <portNumber>"

To start a ttweet client:
    Run "python3 ttweetcli.py <ServerIP> <ServerPort> <Username>" in another command line window

To strat multiple clients:
    Run "python3 ttweetcli.py <ServerIP> <ServerPort> <Username>" in different command line windows

To run command on clients, input following in command line:
    "tweet "<150 char max tweet>"
    "timeline"
    "exit"
