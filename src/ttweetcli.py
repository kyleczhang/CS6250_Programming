import socket
import sys
import getopt
import threading

unread_subscribed_tweets = []

def listening_for_tweets(s):
    while True:
        data = s.recv(1024).decode("utf-8")
        if (not data == "ack" and not data == "nack"):
            unread_subscribed_tweets.append(data)

def main(argv):
    subscriptions = []
    host = ''               # The server's hostname or IP address
    port = ''               # The port used by the server
    username = ''
    hashtag = ''            # hashtag string
    valid_commands = (("tweet",3),("subscribe",2),("unsubscribe",2),("timeline",1),("exit",1))
    '''if( len( sys.argv ) == 1):
        host = '127.0.0.1'
        port = 13069
        username = 'Dril' '''
    if( len( sys.argv ) == 4 ):
        host = sys.argv[1]
        port = sys.argv[2]
        username = sys.argv[3]
    else:
        usage()


    #not working for & but I guess thats life
    if username.isalnum()==False :
        print( 'Username must only contain letters and numbers' )
        sys.exit(2)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect( ( host, int( port ) ) )
            s.sendall( bytes( str ( ( username ) ), 'utf-8' ) )
            data = s.recv(1024)
        except socket.error as msg:
            socketError( msg )
        print( 'Received', repr( data ) )
        if (repr( data ) == "b'error: username already taken'"):
            print("username already taken")
            sys.exit(2)
        else:
            print("username valid, connection estabilished")
            thread = threading.Thread(target=listening_for_tweets, args=(s,))
            thread.daemon = True
            thread.start()
            while(1):
                message = input()
                command = message
                if (command != ''):
                    command_length = len(command.split())
                    if (command.split()[0] == "tweet"):
                        command_length = len(command.split('"'))
                    if ((command.split()[0], command_length) in valid_commands):
                        if (command.split()[0] == "timeline"):
                            if (len(unread_subscribed_tweets) == 0):
                                print ("\n No new tweets")
                            else:
                                print("\nTimeline: ")
                                for tweet in unread_subscribed_tweets:
                                    print(username, "receives message from", tweet)
                                print ('')
                                unread_subscribed_tweets.clear()
                        elif (command.split()[0] == "subscribe"):
                            if ((command.split()[1])[0] != '#' or len(command.split()[1].split('#')) != 2):
                                commandUsage()
                            elif len(command.split()[1]) < 2:
                                hashtagCannotBeOfSizeOne()
                            elif len(command.split()[1]) > 25:
                                hashtagMaxSize()
                            elif len(subscriptions) >= 3:
                                maxSubs()
                            elif command.split()[1] not in subscriptions:
                                subscriptions.append(command.split()[1])
                                s.sendall( bytes( str ( ( command ) ), 'utf-8' ) )
                            else:
                                print("You are already subscribed to this tag")
                            print("Your subscriptions: ",subscriptions)
                        elif command.split()[0] == "unsubscribe":
                            if ((command.split()[1])[0] != '#' or len(command.split()[1].split('#')) != 2):
                                commandUsage()
                            elif command.split()[1] in subscriptions:
                                subscriptions.remove(command.split()[1])
                                s.sendall( bytes( str ( ( command ) ), 'utf-8' ) )
                            else:
                                print("You are not subscribed")
                        elif (command.split()[0] == "tweet"):
                            #only 8 hashtags
                            #max size of 25 per hashtag
                            #only alphanumeric characters
                            tags = command.split('"')[2].split('#')[1:]
                            #print("Tags:",tags)


                            flag = 0
                            flag_2 = 0
                            if (len(tags) == 0):
                                flag = 1
                            for i in range(len(tags)):
                                if len(tags[i]) == 0:
                                    flag = 1
                                if len(tags[i])>24:
                                    flag_2 = 1

                            if ((command.split('"')[2])[1] != '#'):
                                commandUsage()
                            elif (len(command.split('"')[1]) < 1):
                                messageCannotBeEmpty()
                            elif (len(command.split('"')[1]) > 150):
                                messageTooLong(len(command.split('"')[1]))
                            elif flag == 1:
                                hashtagCannotBeOfSizeOne()
                            elif len(tags) > 8:
                                tooManyTags()
                            elif flag_2 == 1:
                                hashtagMaxSize()
                            elif "ALL" in tags:
                                ALLnotAllowedWhenTweeting()
                            else:
                                s.sendall( bytes( str ( ( command ) ), 'utf-8' ) )

                        else:
                            s.sendall( bytes( str ( ( command ) ), 'utf-8' ) )
                            if (command.split('""')[0]  == "exit"):
                                sys.exit(0)
                    else:
                        commandUsage()



def commandUsage():
    print ('\nCommand Usage Error:')
    print ('timeline')
    print ('subscribe #<hastag>')
    print ('unsubscribe #<hastag>')
    print ('tweet "<message <= 150 characters>" [#<hastag>]>')
    print ('exit\n')


def ALLnotAllowedWhenTweeting():
    print("#ALL is not allowed when tweeting")

def tooManyTags():
    print("Only a maximum of 8 tags allowed in a tweet")
def usage():
    print( '\nUsage Error:')
    print( 'Usage:$ python ttweetcli.py <ServerIP> <ServerPort> <Username>\n' )
    sys.exit(2)

def messageTooLong(messageLength):
    print( '\nUsage Error')
    print( 'Messages cannot be longer than 150 charecters, your message is', messageLength , ' characeters long\n' )

def messageCannotBeEmpty():
    print( '\nUsage Error')
    print( 'Messages to be uploaded must not be empty\n')

def hashtagCannotBeOfSizeOne():
    print( '\nUsage Error')
    print( "Hashtag can't be empty\n")

def hashtagMaxSize():
    print( '\nUsage Error')
    print( "Hashtag can't be longer than 24 characters\n")

def socketError(msg):
    print( 'Socket Error' )
    print( msg )
    sys.exit(3)

def maxSubs():
    print("Too many subscriptions.")

main( sys.argv )
