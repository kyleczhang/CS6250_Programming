import sys
import socket
import threading

# {username : conn}
users = {};
hashtags = {};

def run_server(conn,address,user):
    try:
        while conn and user in users.keys():
            data = conn.recv(1024)
            data = repr(data)
            print(data)
            if (data == "b''"):
                raise ConnectionError('Client command error')
            command = data.split()[0]
            # client send tweet to server
            if ("tweet" in command):
                # Get the tweet in the quotations
                tweet = data.split("\"")[1]
                print(tweet)
                tweet = user + ": \"" + tweet + "\"" 
                print(tweet)
                for target in users:
                    if target == user:
                        continue
                    else:   
                        users[target].sendall(bytes(tweet, encoding = "utf-8"))
                rep = "ack"
                conn.send(bytes(rep, encoding = "utf-8"))
            # client send exit request
            elif ("exit" in command):
                # delete the user's info and close the client gracefully
                rep = "exit"
                conn.send(bytes(rep, encoding = "utf-8"))
                conn.close()
                users.pop(user)
                print("Connection with", user, "has been closed")
                break
    except ConnectionError:
        # remove the user from user list and close the client gracefully
        conn.close()
        users.pop(user)
        print("Connection with", user, "has lost because of connection error")
        


def main(argv):
    # get local IP address, the server will listen to local machine
    host = socket.gethostbyname(socket.gethostname())
    # the server will listen to port 8080 by default, it can be replaced by argv[1]
    port = 8080
    # specify port number and check error
    if(len(sys.argv) == 2):
        port = sys.argv[1]
    elif(len(sys.argv) != 2):
        print( 'Usage: $ python3 ttweetsrv.py <port_number>)' )
        sys.exit(1)

    print( 'Server is now listening to', host, ':', port )
    # create socket object that supports the context manager type
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host,int(port)))
        try:
            while (True):
                # set backlog as default
                s.listen()
                # accept and save the client object(conn) and address(addr)
                conn, addr = s.accept()
                # read the 1st data the client sends after logining in
                # this is the user name of the client
                data = conn.recv(1024)
                user = data[0:len(data)].decode("utf-8")
                if (user in users.keys()):
                    conn.send(b'Username has already been taken')
                    conn.close()
                else:
                    users[user] = conn
                    conn.send(b'longin sucessfully')
                    print ("Connected by", user)
                    thread = threading.Thread(target=run_server, args=(conn,addr,user))
                    #thread.daemon = True
                    thread.start()
        except ConnectionError:
            print( user , "disconected" )
            users.remove(user)

if __name__== "__main__":
    main(sys.argv)
