import socket
import sys
import getopt
import threading
import re
import time


mailbox = []

def commandError():
    print ("\nPlease input a valid command:")
    print ('tweet "<150 char max tweet>"')
    print ("timeline")
    print ('exit\n')

"""
listen(s) is used to listen the message from the server
"""
def listen(s):
    while True:
        try:
            data = s.recv(1024).decode("utf-8")
            if (str(data) != "ack"):
                mailbox.append(data)
            if (str(data) == "ack"):
                print("success")
        except socket.error:
            break
    print("Bye bye")


def main(argv):

    # declare data = ""
    data = ""
    # argument error
    if (len(sys.argv) != 4):
        print("Usage: $ python3 ttweetcli.py <ServerIP> <ServerPort> <Username>\n")
        sys.exit(1)
    else:
        serverIP = sys.argv[1]
        serverPort = int(sys.argv[2])
        username = sys.argv[3]
    # username check
    if not re.match("^[A-Za-z0-9]*$", username):
        print("username illegal, username should be made of alphabet characters and numbers")
        sys.exit(1)
    # IP address check
    serverIP_check = serverIP.split(".")
    if(len(serverIP_check) == 4):
        for x in serverIP_check:
            if int(x) < 0 or int(x) > 255:
                print("please input a correct IP address: [0,255].[0,255].[0,255].[0,255]")
                sys.exit(1)
    else:
        print("IPv4 IP address should contain 4 numbers")
        sys.exit(1)

    # port check
    if serverPort < 1 or serverPort > 65535:
        print("port number out of range [0, 65535]")
        sys.exit(1)

    # create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((serverIP, serverPort))
            s.sendall(bytes(username, encoding = "utf-8"))
            data = s.recv(1024)
        except socket.error:
            print("socket error")
            return
        # username check
        data = repr(data)
        if (data == "b'Username has already been taken'"):
            print("user already login, shutdown client")
            sys.exit(1)
        # if the username is not taken, continue the service
        else:
            print("username legal, connection established")
            thread = threading.Thread(target = listen, args = (s,)) #args should be a tuple(an iterable)
            thread.start()
            while (True):
                message = input()
                command = message.split()[0]
                if (command not in ["tweet", "timeline", "exit"]):
                    commandError()
                # tweet "<150 char max tweet>"
                if (command == "tweet"):
                    if (len(message.split('"')[1]) < 1):
                        print("message can not be empty")
                    elif (len(message.split('"')[1]) > 150):
                        print("Message can not be longer than 150 characters")
                    else:
                        s.send(bytes(message, encoding = "utf-8"))


                # timeline
                # <current_client_username> from <sender_username> "<tweet_message>"
                elif command == "timeline":
                    if (len(mailbox) == 0):
                        print ("No new message")
                    else:
                        for tweet in mailbox:
                            print(username, "from", tweet)
                        mailbox.clear()

                # exit
                elif (command == "exit"):
                    s.sendall(bytes(message, encoding = "utf-8"))
                    sys.exit(0)

if __name__ == "__main__":
    main( sys.argv )
