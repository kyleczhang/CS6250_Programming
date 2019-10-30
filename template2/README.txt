i.   Benjamin Yarmowich and Vivian Thiebaut -- TheBestStudent@gatech.edu, vivian.thiebaut@gatech.edu

ii.  CS 3251 Networking: April 2nd 2019 Programming Assignment 2

iii. ttweetsrv.py 		#the server as requested in the documents
     ttweetcli.py 		#the client as requested in the documents
     ttweet_protocol.txt 	#the protocol for ttweet as written
     exampleProgramFlow.png	#a screenshot of the provided example program flow running on the COC shuttles (The shuttle on the right running the server is shuttle 5, the top left is shuttle 3, and the bottom left is shuttle 4)
     sample.png			#a screenshot of a Test Scenario executed on my desktop (server was running on in the bottom right and the clients were running on all other terminals)
     README.txt 		#the document that explains the homework submision

iv. The code for ttweetsrv and ttweetcli are written exclusively in Python 3.7.1 (it should work in all versions of Python greater than 3.6 but I have extensively tested it in 3.7.1)
    If Python3.7.1 is not present on your machine I will provide temporary install instructions for a unix machine below

	If python 3.7.1 is installed but is not currently being pointed to double check the .bashrc file and then run "source ~/.bashrc"

	To run the ttweet program on the shuttles:
		Run "python ttweetsrv.py <port number>"
		Open another tab/window of bash
		Run "python ttweetcli.py <host address> <port number> <username> \
			For full usage documentation run "python ttweetcli.py -usage" 
		To run the commands on the client, use the following formats
		tweet "<tweet message>" #<hashtags>
		subscribe #<hashtag>
		unsubscribe #<hashtag>
		timeline
		exit 


v. For an output sample after running a Test Scenario please see sample.png

vi. See ttweet_protocol.txt for the full protocol description

vii. no bugs are known

How to install Python 3.7.1 on a cc.shuttle:
	Open an ssh connection to the shuttle
	"mkdir ~/python"
	"cd ~/python"
	"wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz"
	"tar zxfv Python-3.7.1.tgz"
	"cd Python-3.7.1/"
	"./configure --prefix=$HOME/python"
	"make"
	"make install"
	"vim ~/.bashrc"
	scroll to the bottom of the file
	"i"
	"export PATH=$HOME/Python-3.7.1/:$PATH"
	":wq"
	"source ~/.bashrc"
	
	now running python --version should return Python 3.7.1

To uninstall:
	"rm -r ~/python"
	"vim ~/.bashrc"
	scroll to the line reading "export PATH=$HOME/python/Python-3.7.1/:$PATH"
	"dd"
	":wq"
	