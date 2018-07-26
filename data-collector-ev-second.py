#!/usr/bin/python

import threading
import sys
import time
from socket import *

print ('*** Data Colector v1.0 ***')
print ('*** miftahf77@gmail.com ***')
print ('*** 24 July 2018 ***')
print ('-----------------------------\n')

# Socket Server Initialization
serverPort = 5000
# Number of clients
n=5
serverSocket = [socket(AF_INET, SOCK_STREAM)]*n
serverIP = '192.168.20.50'
for i in range(n):
    serverSocket[i]=socket(AF_INET, SOCK_STREAM)
    serverSocket[i].setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket[i].bind((serverIP,serverPort + i))
    serverSocket[i].listen(1)
    #print ('success ' + str(i))
print ('Number of client : ' + str(n))
connectionSocket=[0]*n
thread=[0]*n

# Variables to save data for each client
client=[0]*n

# for sending data ev second
evSecThread=''
buff=[0]*n

def main(argv):
    global client,evSecThread
    class myThread (threading.Thread):
       def __init__(self, name, serverSocket, port, no):
          threading.Thread.__init__(self)
          self.name = name
          self.serverSocket = serverSocket
          self.port = port
          self.no = no
       def run(self):
          print ('Port : '+ str(self.port)+ ' for '+ self.name + ' is ready.\n')
          sockData(self.name, self.serverSocket, self.port, self.no)
          
    class evSecondThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
        def run(self):
            sendData()

    # Sending data every second
    def sendData():
        global collector,buff,n
        buff2=[0]*n
        data_ev_sec=[0]*n
        while 1:
            time.sleep(1)
            for i in range(n):
                data_ev_sec[i]=buff[i]-buff2[i]
                buff2[i]=buff[i]
                # Overflow Checking
                if buff[i]>=5000000:
                    buff[i]=0
                    buff2[i]=0
            print (data_ev_sec)

    # Get data from all clients
    def sockData( name, serverSocket, port, no):
        global client,buff
        try:
            while 1:
                # Accept connection from client (blocking mode)
                connectionSocket[no], addr = serverSocket.accept()
                #print(connectionSocket.getpeername())
                #print (name + ' , Port : ' + str(port))
            
                # Receives data message from Socket Client
                msg=connectionSocket[no].recv(1024)
                msg=msg.decode('ascii')
                print (msg)
                # Parsing msg
                # Get data for each client
                client[no]=msg
                buff[no]=buff[no]+1

                # Sends ACK message to Client
                connectionSocket[no].send('ack'.encode('utf-8'))
                while 1:
                    try:
                        msg=connectionSocket[no].recv(32)
                        msg=msg.decode('ascii')
                    except:
                        print (name + ' is closed!')
                        connectionSocket[no].close()
                        break
                    if msg=='ok':
                        connectionSocket[no].close()
                        break
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

    # Create new thread for sending data every second
    try:
        evSecThread=evSecondThread()
    except Exception as e:
        print ("Error: unable to start thread!")
        print (str(e))

    # Start new Threads
    for i in range(n):
        thread[i].start()
    # Start new thread for sending data ev second
    evSecThread.start()
    
    while 1:
        pass

if __name__=="__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print (str(e))


# Note :
# For this data collector script will send data at every second, doesn't matter if all data are received or not.
