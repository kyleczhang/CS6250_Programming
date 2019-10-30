Worked done by 
Chawalit Saetiew,
GTID: 903197479,
campusID: csaetiew3

How to use:

Run the server by entering "python2 ttweetsrv.py <port_number>" into the commandline

Run the client by entering "python2 ttweetcl.py <ServerIP> <ServerPort> <Username>" into the command line

Suported commands are:

Server: No input supported. 

Client:
subscribe <Hashtag>
unsubscribe <Hashtag>
tweet “<150 char max tweet>” <HashtagHashtag> #May have mutliple hashtags within
timeline
exit

Packages needed:
socket
thread
sys

Implementation Idea:
Client: The input is sent to the server to handle except for timeline and tweet.
The client has access to the message box, so the client can print then delete the messages.
The tweet command contains the message that needs to be checked for corrrect length before sending it

The client receives data from the server after sending the command. It receives error and success codes
that allow the client to print feedback to the user or take action such as printing out a message 
and adding that message to the message box.

The client has a nonblocking input by creating a thread to handle the input. The thread method also has
access to the message box so the spawned thread can handle the input command without returning to the 
main method.

Server: When a client requests to communicate, the server creates a thread to handle the client.
All transactions will then be handled by that thread. The main method is only responsible for 
accepting socket and creating a new thread for that socket

In the thread on_new_client, the command is obtained by parsing the message sent by the client
The command is put in an if statement to find the correct action. The code inside the if statements
call the correct method to handle what the client wants. Each method returns True or False to 
indicate success or failure. The server then sends a respose to the client to say that its 
command is successful or not

Information on the server is kept in dictionaries with the user name as the key, and information
regarding that user as the data. Some other dictionary have a different key such as the address of
the user. This is how information about other clients is accessable when a client wants to tweet.

Commands such as subscribe, unsubscribe, and exit modify these dictionaries and lists.
