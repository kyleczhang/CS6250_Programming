import socket
import sys
import threading
import re

users = {};
hashtags = {};


def error(code):
    if( code == 1 ):
        print( "data recieved was null" )
    sys.exit(2)

def usage():
    print( 'Usage: $ ./ttweetsrv.py <port>)' )
    sys.exit(2)

def handle_client(connection,address,user):
    try:
        while connection and user in users.keys():
            data = connection.recv(1024)
            data = repr( data )
            if (data == "b''"):
                raise ConnectionError('keyboard end connection')
            if ("tweet" in data.split()[0]):
                tweet = data.split('"')[1]
                tags = data.split('"')[2][:-1].split('#')[1:]

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
                connection.sendall( b'ack')
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
    host = socket.gethostbyname(socket.gethostname()) # Default host ip address (localhost)
    port = 13069        # Default port to listen on
    if( len( sys.argv ) == 2):
        port = sys.argv[1] # Allows the user to override default host and port #
    elif( len( sys.argv ) != 2): #changed from >2 to !=2 because according to PDF if can accept ONE (in bold) argument
        usage()
    print( 'Connected at', host, ':', port )
    with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as s:
        try:
            s.bind( ( host, int( port ) ) ) # Binds the server to the specified host and port
            while True:
                s.listen(1)                     # Server is now listening on the bound host and port
                conn, addr = s.accept()         # On connection request, complete the three way handshake
                data = conn.recv(1024)  # Handles recieving messages of any length

                user = data[0:len( data )].decode("utf-8")
                if ( user in users.keys() ):
                    conn.sendall( b'error: username already taken' )
                    conn.close()
                else:
                    users[user] = conn
                    conn.sendall( b'you have sucessfully connected' )
                    print ("Connection estabilished with", user)
                    thread = threading.Thread(target=handle_client, args=(conn,addr,user))
                    thread.daemon = True
                    thread.start()
        except socket.error as msg:
            if ( msg.errno == 98 ):
                print( "Server Socket Error" )
                print( msg )
                err98_handler = True
            if ( msg.errno != 98 ):
                print( "Server Socket Error" )
                print( msg )
        except ConnectionError as error:
            print( user , "disconected" )
            users.remove(user)



main(sys.argv)
