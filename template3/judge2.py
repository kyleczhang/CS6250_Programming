# -*- coding:utf-8 -*-
import os
import subprocess
import signal
import time


class judge:
    """
    This is the driver script for GT CS3251, programming assignment 2, 2019 spring
    Don't worry if your program can't be run by this script, we will test your program manually on shuttle machine
    The usage of this script is, put this script under the same folder as your program(not source code, the executable program)

    run:
    python2 judge2.py <type>

    The type mapping depends on your programming language:
    {'j':'java ', 'p':'python2 ', 'c':'./', 'jar': 'java -jar '}

    The default port number for the driver is 13000

    feel free to comment or uncomment some functions to test only one part

    feel free to do modifications on this script

    Tips:
    1. there will be several strange cases that the script failed to start your server, you could start your server manually
    under this situation with srv=False in function call
    2. The full test will cost about 10 minuates, so please be patient
    3. I want to say again this is only a test script, no worry if your program failed, we will test manually on shuttle machine
    shuttle machine is the final judger!
    4. Since you have got this script, I will also make some more test cases based on this script


    Best,
    Xiang

    """

    def __init__(self):
        self.run={'j':'java ', 'p':'python2 -u ', 'c':'./', 'jar': 'java -jar '}
        if(os.path.exists('client.txt')):
            os.remove('client.txt')
        if (os.path.exists('server.txt')):
            os.remove('server.txt')
        self.file = open('client.txt', 'w')
        self.server = open('server.txt', 'w')

    def get_msg(self):
        messages = [ ' ', 'cs3251', 'fsadfsdfd','empty message', 'message', 'Empty Message','d','u','download']

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
        messages = [ ' ', 'cs3251', 'fsadfsdfd','empty message']

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
        print("in test_single_client")
        self.file.write('test_single_client\n')
        self.file.flush()
        username = 'cxworks'
        cmd=self.run[type] + name + ' 127.0.0.1 %d %s' % (port, username)
        self.file.write('\nrun command: ' + cmd + '\n')
        self.file.flush()
        p = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
        time.sleep(1)
        postfix=['tweet "" #hash', 'tweet "message" #hash', 'tweet "message message" #hash']
        for post in postfix:
            self.input_stdin(p, post, username)

        subs='subscribe #echo'
        self.input_stdin(p, subs, username)
        cmd_template = 'tweet "%s" #echo'
        for msg in self.get_msg():
            cmd = cmd_template % msg
            self.input_stdin(p, cmd, username)
        unsub = 'unsubscribe #echo'
        self.input_stdin(p, unsub, username)
        for msg in self.get_msg():
            cmd = cmd_template % msg
            self.input_stdin(p, cmd, username)
        timeline = 'timeline'
        self.input_stdin(p, timeline, username)
        ex = 'exit'
        self.input_stdin(p, ex, username)

        self.file.write('test_single_client _ end\n\n')
        self.file.flush()


    def test_multi_client(self, type, name, port):
        print("in test_multi_client")

        self.file.write('test_multi_client\n')
        self.file.flush()
        MAX_CLIENT_NUM = 5
        username = 'cxworks'
        processes = {}
        for i in range(MAX_CLIENT_NUM):
            cmd = self.run[type] + name + ' 127.0.0.1 %d %s' % (port, username+str(i))
            self.file.write('\nrun command: ' + cmd + '\n')
            self.file.flush()
            p = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
            time.sleep(1)
            processes[username+str(i)] = p

        postfix = ['tweet "" #hash', 'tweet "message" #hash', 'tweet "message message" #hash']
        for post in postfix:
            for k, p in processes.items():
                self.input_stdin(p, post, k)

        subs = 'subscribe #echo'
        for k, p in processes.items():
            self.input_stdin(p, subs, k)
        cmd_template = 'tweet "%s" #echo'
        for msg in self.get_msg_small():
            cmd = cmd_template % msg
            for k,p  in processes.items():
                self.input_stdin(p, cmd, k)
        unsub = 'unsubscribe #echo'
        for k,p  in processes.items():
            self.input_stdin(p, unsub, k)
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
        print("in test_logic")

        # test dup username
        username = 'cxworks'
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


        # test subscribe ALL tag & multi tags
        username = 'cs3251'
        cmd = self.run[type] + name + ' 127.0.0.1 %d %s' % (port, username)
        self.file.write('\nrun command: ' + cmd + '\n')
        self.file.flush()
        p_all = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
        time.sleep(1)
        self.input_stdin(p_all, 'subscribe #ALL', username)

        MAX_CLIENT_NUM = 5
        processes = {}
        for i in range(MAX_CLIENT_NUM - 1):
            cmd = self.run[type] + name + ' 127.0.0.1 %d %s' % (port, username + str(i))
            self.file.write('\nrun command: ' + cmd + '\n')
            self.file.flush()
            p = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
            time.sleep(1)
            processes[username + str(i)] = p
        subs = 'subscribe #%d'
        counter=0
        for k, p in processes.items():
            self.input_stdin(p, subs % counter, k)
            counter+=1

        cmd_template = 'tweet "%s" #%d#%d'
        counter=0
        for k, p in processes.items():
            for i in range(MAX_CLIENT_NUM - 1):
                idx = int((counter+i)%(MAX_CLIENT_NUM - 1))
                next = int((counter+i + 1)%(MAX_CLIENT_NUM - 1))
                for msg in self.get_msg_small():
                    cmd = cmd_template % (msg, idx, next)
                    self.input_stdin(p, cmd, k)



        self.input_stdin(p_all, 'unsubscribe #ALL', username)

        cmd_template = 'tweet "%s" #%d#%d'
        counter = 0
        for k, p in processes.items():
            for i in range(MAX_CLIENT_NUM - 1):
                idx = int((counter + i) % (MAX_CLIENT_NUM - 1))
                next = int((counter + i + 1) % (MAX_CLIENT_NUM - 1))
                for msg in self.get_msg_small():
                    cmd = cmd_template % (msg, idx, next)
                    self.input_stdin(p, cmd, k)

        timeline = 'timeline'
        for k, p in processes.items():
            self.input_stdin(p, timeline, k)
        self.input_stdin(p_all, timeline, username)
        timeline = 'timeline'
        for k, p in processes.items():
            self.input_stdin(p, timeline, k)
        self.input_stdin(p_all, timeline, username)

        ex = 'exit'
        for k, p in processes.items():
            self.input_stdin(p, ex, k)
        self.input_stdin(p_all, ex, username)

        # test subscribe more than 3 tags
        cmd = self.run[type] + name + ' 127.0.0.1 %d %s' % (port, username)
        self.file.write('\nrun command: ' + cmd + '\n')
        self.file.flush()
        p = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
        time.sleep(1)
        subs = 'subscribe #%dlove3251'
        for i in reversed(range(10)):
            self.input_stdin(p, subs % i, username)

        cmd = self.run[type] + name + ' 127.0.0.1 %d %s' % (port, 'sender')
        self.file.write('\nrun command: ' + cmd + '\n')
        self.file.flush()
        p_sender = subprocess.Popen(cmd, shell=True, stdout=self.file, stdin=subprocess.PIPE)
        time.sleep(1)
        for msg in self.get_msg_small():
            for i in range(10):
                cmd = 'tweet "%s" #%s' % (msg, str(i)+'love3251')
                self.input_stdin(p_sender, cmd, 'sender')
        self.input_stdin(p_sender, 'exit', 'sender')
        self.input_stdin(p, timeline, username)
        self.input_stdin(p, timeline, username)
        self.input_stdin(p, 'exit', username)




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
        print("in test_no_server")
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
        print("in test_illegal_input")

        self.file.write('test_illegal_input\n')
        self.file.flush()
        cmds=[' ', ' 127.0.0.1',' 324.1.1.4', ' 127.0.0.1 -3', ' 127.0.0.1 80 ', ' 127.0.0.1 13001 ']
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


    def runTest(self, type, srv = True, port=13001):
        client_names={'j':'ttweetcl','p':'ttweetcl.py','c':'ttweetcl', 'jar': 'ttweetcl.jar'}
        srv_names = {'j': 'ttweetsrv', 'p': 'ttweetsrv.py', 'c': 'ttweetsrv', 'jar': 'ttweetsrv.jar'}

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
    judge().runTest(args[1], True, 13001)
