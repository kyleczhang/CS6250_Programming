import socket
import sys
import threading
import re

# {user:conn}
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

                for i in range(len(tags)):
                    tags[i] = '#'+tags[i]

                print (tags)
                tweet = str(user) + ": " + str(tweet) + ' ' + ''.join(tags)
                print (tweet)
                usersTweetSentTo = []
                for tag in tags:
                    if (tag in hashtags.keys()):
                        for u in hashtags[tag]:
                            if (u not in usersTweetSentTo):
                                usersTweetSentTo.append(u)
                                users[u].sendall( bytes( str ( ( tweet ) ), 'utf-8' ) )
                if "#ALL" in hashtags.keys():
                    for u in hashtags["#ALL"]:
                        if u not in usersTweetSentTo:
                            usersTweetSentTo.append(u)
                            users[u].sendall( bytes( str ( ( tweet ) ), 'utf-8' ) )

                print(tags)
                conn.sendall( b'ack')
            elif ("unsubscribe" in data.split()[0]):
                tag = '#' + data.split()[1][1:-1]
                print ("unsubscribe" , tag)
                if (tag in hashtags.keys() and user in hashtags[tag]):
                    hashtags[tag].remove(user)
                    connection.sendall( b'ack')
                else:
                    connection.sendall( b'nack')
                print (hashtags)
            elif ("subscribe" in data.split()[0] and len(data.split()[1][1:-1]) > 0):
                tag = '#'+ data.split()[1][1:-1]
                print ("subscribe" , tag)
                if (tag in hashtags.keys() and user in hashtags[tag]):
                    connection.sendall( b'nack')
                elif (tag in hashtags.keys()):
                    hashtags[tag].append(user)
                    connection.sendall( b'ack')
                else:
                    hashtags[tag] = []
                    hashtags[tag].append(user)
                    connection.sendall( b'ack')
                print (hashtags)

            elif ("exit" in data.split()[0]):
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
