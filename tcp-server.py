#!/usr/bin/python

import threading
import sys
from socket import *

# Socket Server Initialization
serverPort = 5000
# Number of clients
n=5
serverSocket = [socket(AF_INET, SOCK_STREAM)]*n
serverIP = '169.254.148.241'
for i in range(n):
    serverSocket[i]=socket(AF_INET, SOCK_STREAM)
    serverSocket[i].setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket[i].bind((serverIP,serverPort + i))
    serverSocket[i].listen(1)
    print ('success ' + str(i))
connectionSocket=[0]*n
thread=[0]*n

# Variables to save data for each client
client=[0]*n

def main(argv):
    class myThread (threading.Thread):
       def __init__(self, name, serverSocket, port, no):
          threading.Thread.__init__(self)
          self.name = name
          self.serverSocket = serverSocket
          self.port = port
          self.no = no
       def run(self):
          print (self.name + ' is ready.\n')
          sockData(self.name, self.serverSocket, self.port, self.no)
          
    def sockData( name, serverSocket, port, no):
        try:
            while 1:
                # Accept connection from client
                connectionSocket[no], addr = serverSocket.accept()
                #print(connectionSocket.getpeername())
                print (name + ' , Port : ' + str(port))

                # Receives data message from Socket Client
                msg=connectionSocket[no].recv(1024)
                msg=msg.decode('ascii')
                # print (msg)

                # Sends ACK message to Client
                connectionSocket[no].send('ack'.encode('utf-8'))
                while 1:
                    try:
                        msg=connectionSocket[no].recv(32)
                        msg=msg.decode('ascii')
                        # Get data for each client
                        client[no]==msg
                    except:
                        print (name + ' is closed!')
                        connectionSocket[no].close()
                        break
                    if msg=='ok':
                        connectionSocket[no].close()
                        break
                print (client)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print (str(e))

    # Create new threads
    try:
        for i in range(n):
            name="Client-"+str(i)
            thread[i] = myThread(name, serverSocket[i], serverPort+i, i)
    except Exception as e:
            print ("Error: unable to start thread!")
            print (str(e))

    # Start new Threads
    for i in range(n):
        thread[i].start()
    while 1:
        pass

if __name__=="__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print (str(e))
