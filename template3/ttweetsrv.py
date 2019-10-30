import socket
import thread
import sys

# Use of thread format comes from https://stackoverflow.com/questions/10810249/python-socket-multiple-clients

# 
current_users = []  # list of users in str
addr_user = {}      # address to user dictionary
user_tags = {}      # user to tag dictionary
user_socket = {}    # user to socket


# Method that runs on a new thread when a client connects
def on_new_client(clientsocket,addr):
    # Username
    user = ""
    while True:
        msg = clientsocket.recv(1024)
        command = msg.split(" ")[0] # retrieves the first str which is the command

        if command == "exit": 
            if exit(clientsocket, addr, user): # go to exit method for clean up
                ret = "exited"
                clientsocket.send(ret.encode("utf-8")) # return success to client

        elif command == "tweet":

            # Obtains the message within quotations
            # Also allows quotation marks within the message
            message_array = msg.split("\"")
            new_message = ""
            print(message_array)
            for x in range(1, len(message_array) - 1):
                new_message += message_array[x]
            tag = message_array[len(message_array) - 1][1:]


            tweet(clientsocket, addr, new_message, tag) # calls tweet method

            ret = "succ3"
            clientsocket.send(ret.encode("utf-8")) #return success
        

        elif command == "login":
            username = msg.split(" ")[1] # gets username when first connecting
            user = username
            if not login(clientsocket, addr, user): # if username is already taken
                print("login failed")
                ret = "err0"
                clientsocket.send(ret.encode("utf-8")) # return error to client
                break
            else:
                print("login succeded")
                ret = "succ0"
                clientsocket.send(ret.encode("utf-8")) # return successful login to client

        elif command == "subscribe":
            tag = msg.split(" ")[1] # obtain the tag of the client

            if not subscribe(clientsocket, addr, tag, user): # calls the subscribe tag
                print("subscription failed") # subscription to tag failed
                ret = "err1 " + tag
                clientsocket.send(ret.encode("utf-8")) # return error to client
            else:
                print("subscription succeded")
                ret = "succ1 " + tag
                clientsocket.send(ret.encode("utf-8")) # return success to client

        elif command == "unsubscribe":
            tag = msg.split(" ")[1] # obtain the tag of the client
            if not unsubscribe(clientsocket, addr, tag, user): # removal failed
                print("unsubscription failed")
                ret = "err2 " + tag
                clientsocket.send(ret.encode("utf-8")) # send error to client
            else:
                print("unsubscription succeded")
                ret = "succ2 " + tag
                clientsocket.send(ret.encode("utf-8")) # send success to client
        else:
            ret = "err5"
            clientsocket.send(ret.encode("utf-8")) # the command is not supported
    clientsocket.close()

# Logs the user in
def login(clientsocket, addr, username):
    print("on login")

    # Checks if the username is already taken
    # return False if taken
    for user in current_users:
        if username == user:
            return False
    print("  " + username)

    # initialize all list and dictionaries for the user and the addr
    addr_user[addr] = username
    current_users.append(username)
    user_tags[username] = []
    user_socket[username] = clientsocket

    print(current_users)
    return True

# Cleans up the list and dictionary for the user
def exit(clientsocket, addr, username):
    print("on exit")
    current_users.remove(username)
    user_tags.pop(username, None)
    user_socket.pop(username, None)
    addr_user.pop(addr, None)
    return True

# Tweets the message for the following tags
def tweet(clientsocket, addr, message, tags):
    print("on tweet")
    print(tags)
    # Splits the tags into a list and append #ALL
    tags_tweeted = tags.split("#")
    tags_tweeted.append("ALL")
    print(tags_tweeted)

    # For every user check the tags to see if there is a match
    for user in user_tags:
        target = False
        for tag in user_tags[user]:
            if target:
                break
            for tag_tweeted in tags_tweeted:
                if target:
                    break
                # If match, then send message to the target then move on to a new user
                if tag == tag_tweeted or tag == "ALL": 
                    target = True
                    twt = "succ5 " + message + " from " + addr_user[addr] + " with " + tags
                    user_socket[user].send(twt.encode("utf-8"))
                    break
    return True

# subscribes to the tag
def subscribe(clientsocket, addr, tag, username):
    # remove #
    tag = tag[1:]
    print("on subscribe")

    # checks if the tag already exists 
    current_tags = user_tags[username]
    for subbed_tag in current_tags:
        if subbed_tag == tag:
            return False
    # checks the current amount of subscribed tags
    if len(current_tags) == 3:
        return False
    user_tags[username].append(tag)
    return True

        
# unsubscribes from the tag
def unsubscribe(clientsocket, addr, tag, username):
    # remove #
    tag = tag[1:]
    print(tag)
    print("on unsubscribe")
    # Find the tag, remove, and return true, else return false
    current_tags = user_tags[username]
    for subbed_tag in current_tags:
        if subbed_tag == tag:
            user_tags[username].remove(subbed_tag)
            return True
    return False

def timeline(clientsocket, addr, msg):
    print("on timeline")
    return


def main():
    # Check the number of arguement
    if len(sys.argv) !=2:
        print("python ttweetsrv.py <Port>")
        
    # Checks the port number range
    if int(sys.argv[1]) < 0 or int(sys.argv[1]) > 65535:
        print("port number should be in [1,65535]")
        return

    s = socket.socket()         # Create a socket object
    host = '127.0.0.1'          # Set local host addr
    port = int(sys.argv[1])     # Set port number

    print ('Server started!')
    print ('Waiting for clients...')

    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # listen for client connection.

    while True:
        # if current users is 5 or greater, don't accept anymore connections
        if len(current_users) >= 5:
            continue
        c, addr = s.accept()     # Establish connection with client.
        thread.start_new_thread(on_new_client,(c,addr)) # send clientsocket to the thread

    s.close()

if __name__== "__main__":
    main()