#!/usr/bin/python

import threading
import sys
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

# Variables for queue
m=1000    # Max queue of data
que=[[0 for i in range(m)] for i in range(n)]
inc=[0]*n
zero_f=0
first_run_f=0

def main(argv):
    global m,que,inc,zero_f,client,first_run_f
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
          
    def sockData( name, serverSocket, port, no):
        global m,que,inc,zero_f,client,first_run_f
        try:
            while 1:
                # Accept connection from client
                connectionSocket[no], addr = serverSocket.accept()
                #print(connectionSocket.getpeername())
                #print (name + ' , Port : ' + str(port))

                # Receives data message from Socket Client
                msg=connectionSocket[no].recv(1024)
                msg=msg.decode('ascii')
                # print (msg)
                # Get data for each client
                if inc[no]==m:
                    # Reset inc var for each client
                    inc[no]=0
                # client[no]=msg
                que[no][inc[no]]=msg
                if first_run_f==1:
                    inc[no]=inc[no]+1

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
                # Check if there is a zero value in data variable
                for i in range(n):
                    if que[i][0]==0:
                        zero_f=1
                    else:
                        # print (que)
                        client[i]=que[i][0]
                if zero_f==0:
                    # Shift operation in queue
                    for i in range(n):
                        inc[i]=inc[i]-1
                        for j in range(m):
                            if j<m-1:
                                que[i][j]=que[i][j+1]
                            elif j==m-1:
                                que[i][j]=0
                    print (client)
                    # Make zero data variable
                    for i in range(n):
                        client[i]=0
                    first_run_f=1
                else :
                    zero_f=0
                    if first_run_f==1:
                        print ('Not all data are received!')
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


# Note :
# For this data collector script will use queue to send all data a once. So the system will wait untill all data is received by buffer and then will send all data received at once.
