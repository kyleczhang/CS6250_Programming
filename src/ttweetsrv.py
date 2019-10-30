import socket
import sys
import threading
import re

# {username : conn}
users = {};
hashtags = {};


def dataError(code):
    if( code == 1 ):
        print( "data recieved was null" )
    sys.exit(1)

def usageError():
    print( 'Usage: $ python3 ttweetsrv.py <port_number>)' )
    sys.exit(1)

def run_server(conn,address,user):
    try:
        while conn and user in users.keys():
            data = conn.recv(1024)
            data = repr(data)
            if (data == "b''"):
                raise ConnectionError('Client command error')
            command = data.split()[0]
            # client send tweet to server
            if (command == "tweet"):
                # Get the tweet in the quotations
                tweet = data.split("\"")[1]                
                for target in users[]:
                    if target == user:
                        continue
                    else:
                        users[target].sendall(tweet.encode("utf-8"))
                conn.sendall(b'ack')

            elif (command == "exit"):
                #TODO: Remove user and connection from all subscriptions
                for tag in hashtags.keys():
                    if user in hashtags[tag]:
                        hashtags[tag].remove(user)
                users.pop(user)
                connection.close()
                print("Connection closed with", user)
                #print (hashtags)
                #print (users)
                break
    except ConnectionError as error:
        #TODO: Remove user and connection from all subscriptions
        for tag in hashtags.keys():
            if user in hashtags[tag]:
                hashtags[tag].remove(user)
        print( user , "disconected" )
        connection.close()
        users.pop(user)


def main(argv):
    # get local IP address, the server will listen to local machine
    host = socket.gethostbyname(socket.gethostname())
    # the server will listen to port 8080 by default, it can be replaced by argv[1]
    port = 8080
    # specify port number and check error
    if(len(sys.argv) == 2):
        port = sys.argv[1]
    elif(len(sys.argv) != 2):
        usageError()
    print( 'Server is now listening to', host, ':', port )
    # create socket object that supports the context manager type
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host,int(port)))
        try:
            while True:
                # set backlog as default
                s.listen()
                # accept and save the client object(conn) and address(addr)
                conn, addr = s.accept()
                # read the 1st data the client sends after logining in
                # this is the user name of the client
                data = conn.recv(1024)
                user = data[0:len(data)].decode("utf-8")
                if (user in users.keys()):
                    conn.sendall(b'Username has already been taken')
                    conn.close()
                else:
                    users[user] = conn
                    conn.sendall( b'You have sucessfully connected to the server')
                    print ("Connected by", user)
                    thread = threading.Thread(target=run_server, args=(conn,addr,user))
                    #thread.daemon = True
                    thread.start()
        except ConnectionError:
            print( user , "disconected" )
            users.remove(user)

if __name__== "__main__":
    main(sys.argv)
