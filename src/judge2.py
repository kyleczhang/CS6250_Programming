# -*- coding:utf-8 -*-
import os
import subprocess
import signal
import time


class judge:
    """
    This is the driver script for GT CS6250, programming assignment, 2019 fall
    Don't worry if your program can't be run by this script, we will test your program manually on shuttle machine
    The usage of this script is, put this script under the same folder as your program(not source code, the executable program)

    run:
    python judge2.py <type>

    The type mapping depends on your programming language:
    {'j':'java ', 'p2':'python2 ', 'p3':'python3 ', 'c':'./', 'jar': 'java -jar '}

    The default port number for the driver is 13000

    feel free to comment or uncomment some functions to test only one part

    feel free to do modifications on this script

    Tips:
    1. There will be several strange cases that the script failed to start your server, you could start your server manually
    under this situation with srv=False in function call
    2. The full test will cost about 5 minuates, so please be patient
    3. I want to say again this is only a test script, no worry if your program failed, we will test manually on shuttle machine
    shuttle machine is the final standard!
    4. Since you have got this script, I will also make some more test cases based on this script


    Best,
    Xiang

    """

    def __init__(self):
        self.run={'j':'java ', 'p2':'python2 -u ', 'p3':'python3 -u ', 'c':'./', 'jar': 'java -jar '} # For python, -u to disable output buffering
        if(os.path.exists('client.txt')):
            os.remove('client.txt')
        if (os.path.exists('server.txt')):
            os.remove('server.txt')
        self.file = open('client.txt', 'w')
        self.server = open('server.txt', 'w')

    def get_msg(self):
        messages = [ ' ', 'cs6250', 'fsadfsdfd','empty message', 'message', 'Empty Message','d','u','download']

        symbols = '~!@#$%^&*()_+-=[]{};:.,<>/?|\\'
        for s in symbols:
            messages.append(s)
        messages.append('\\0')
        for i in range(149,152):
            s=''.join(['a' for _ in range(i-3)])
            messages.append(str(i)+s)
            messages.append(''.join([' ' for _ in range(i)]))
        messages = messages[:-1]
        for m in messages:
            yield m

    def get_msg_small(self):
        """
        generator for messages to test, this will generate less messages than previous function
        :return:
        """
        messages = [ ' ', 'cs6250', 'fsadfsdfd','empty message']

        symbols = '~!@#$%^&*()_+-=[]{};:.,<>/?|\\'
        messages.append(symbols)
        messages.append('\\0')
        for i in range(149,152):
            s=''.join(['a' for _ in range(i-3)])
            messages.append(str(i)+s)
            messages.append(''.join([' ' for _ in range(i)]))
        messages = messages[:-1]
        for m in messages:
            yield m

    def test_single_client(self, type, name, port):
        self.file.write('test_single_client\n')
        self.file.flush()
        username = 'network'
        cmd=self.run[type] + name + ' 127.0.0.1 %d %s' % (port, username)
        self.file.write('\nrun command: ' + cmd + '\n')
        self.file.flush()
        p = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
        time.sleep(1)
        postfix=['tweet ""', 'tweet "message"', 'tweet "message message"']
        for post in postfix:
            self.input_stdin(p, post, username)


        timeline = 'timeline'
        self.input_stdin(p, timeline, username)
        ex = 'exit'
        self.input_stdin(p, ex, username)

        self.file.write('test_single_client _ end\n\n')
        self.file.flush()


    def test_multi_client(self, type, name, port):
        self.file.write('test_multi_client\n')
        self.file.flush()
        MAX_CLIENT_NUM = 5
        username = 'network'
        processes = {}
        for i in range(MAX_CLIENT_NUM):
            cmd = self.run[type] + name + ' 127.0.0.1 %d %s' % (port, username+str(i))
            self.file.write('\nrun command: ' + cmd + '\n')
            self.file.flush()
            p = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
            time.sleep(1)
            processes[username+str(i)] = p

        postfix = ['tweet ""', 'tweet "message"', 'tweet "message message"']
        for post in postfix:
            for k, p in processes.items():
                self.input_stdin(p, post, k)


        cmd_template = 'tweet "%s"'
        for msg in self.get_msg_small():
            cmd = cmd_template % msg
            for k,p  in processes.items():
                self.input_stdin(p, cmd, k)

        for msg in self.get_msg_small():
            cmd = cmd_template % msg
            for k,p in processes.items():
                self.input_stdin(p, cmd, k)
        timeline = 'timeline'
        for k,p in processes.items():
            self.input_stdin(p, timeline, k)

        timeline = 'timeline'
        for k, p in processes.items():
            self.input_stdin(p, timeline, k)
        ex = 'exit'
        for k,p in processes.items():
            self.input_stdin(p, ex, k)

        self.file.write('test_multi_client _ end\n\n')
        self.file.flush()

    def test_logic(self, type, name, port):
        # test dup username
        username = 'gtnetwork'
        cmd = self.run[type] + name + ' 127.0.0.1 %d %s' % (port, username )
        self.file.write('\nrun command: ' + cmd + '\n')
        self.file.flush()
        p1 = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
        time.sleep(1)
        # now, same user can't be login

        self.file.write('\nrun command on same user: ' + cmd + '\n')
        self.file.write('this step should be failed\n')
        self.file.flush()
        p2 = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
        time.sleep(1)
        # logout p1
        self.input_stdin(p1, 'exit', username)
        # now second user should login successfully
        self.file.write('\nrun command on same user: ' + cmd + '\n')
        self.file.write('this step should succeed\n')
        self.file.flush()
        p2 = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
        time.sleep(1)
        self.input_stdin(p2, 'exit', username)






    def input_stdin(self, p, cmd, username):
        self.file.write('\nuser %s stdin command: ' % username + cmd + '\n')
        self.file.flush()
        cmd=cmd+'\n'
        try:
            p.stdin.write(cmd.encode())
            p.stdin.flush()
            time.sleep(0.1)
        except Exception as e:
            print(e)
            self.file.write('error happens\n')
            self.file.flush()

    def test_no_server(self, type, name, port):
        self.file.write('test_no_server\n')
        self.file.flush()
        cmds=[' 127.0.0.1 %d cxworks' % port]
        for postfix in cmds:
            cmd = self.run[type] + name + postfix
            self.file.write('\nrun command: '+ cmd +'\n')
            self.file.flush()
            try:
                subprocess.call(cmd, stdout=self.file, stderr=self.file, shell=True)
            except Exception:
                self.file.write('error happens\n')
                self.file.flush()
        self.file.write('test_no_server _ end\n\n')
        self.file.flush()

    def test_illegal_input(self, type, name):
        self.file.write('test_illegal_input\n')
        self.file.flush()
        cmds=[' ', ' 127.0.0.1',' 324.1.1.4', ' 127.0.0.1 -3', ' 127.0.0.1 80 ', ' 127.0.0.1 13000 ']
        for postfix in cmds:
            cmd = self.run[type] + name + postfix
            self.file.write('\nrun command: '+ cmd +'\n')
            self.file.flush()
            try:
                subprocess.call(cmd, stdout=self.file, stderr=self.file, shell=True)
            except Exception:
                self.file.write('error happens\n')
                self.file.flush()
        self.file.write('test_illegal_input _ end\n\n')
        self.file.flush()



    def start_server(self,type, name, port):

        p = subprocess.Popen(self.run[type] + name + ' ' + str(port),stdout=self.server, stderr=self.server, shell=True)
        time.sleep(1)
        self.file.write('run command on server: '+ self.run[type] + name + ' ' + str(port) + '\n')
        self.file.flush()
        time.sleep(0.1)
        return p


    def runTest(self, type, srv = True, port=13000):
        client_names={'j':'ttweetcli','p2':'ttweetcli.py', 'p3':'ttweetcli.py', 'c':'ttweetcli', 'jar': 'ttweetcli.jar'}
        srv_names = {'j': 'ttweetsrv', 'p2': 'ttweetsrv.py', 'p3': 'ttweetsrv.py', 'c': 'ttweetsrv', 'jar': 'ttweetsrv.jar'}

        if(srv):
            self.test_no_server(type, client_names[type], port)
            # start server
            p = self.start_server(type, srv_names[type], port)
        else:
            t = input('Please start your server manually, then press Enter to continue')


        self.test_illegal_input(type, client_names[type])
        self.test_single_client(type, client_names[type], port)
        self.test_multi_client(type, client_names[type], port)
        self.test_logic(type, client_names[type], port)
        if(srv):
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        if(not srv):
            t = input('Please close your server manually, then press Enter to continue')
            self.test_no_server(type, client_names[type])

        self.file.close()
        self.server.close()



if __name__ == '__main__':
    import sys
    args = sys.argv
    judge().runTest(args[1], True, 13000)
