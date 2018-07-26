# Socket Test Program

from socket import *
# For testing
import random
import time

## Client Socket Communication initialization
serverIP = '192.168.10.250'    # PC Server IP
serverPort = 5003               # PC Server Port
sensorNo=15
sen=[0]*15
line=4

n=0
e_f=0
while 1:
    i=0
    while i <= 50000:
        i=i+1
    try:
        # Using Socket Connection to send all data from PLC to PC Server
        while 1:
            try:
                clientSocket=socket(AF_INET, SOCK_STREAM)
                clientSocket.connect((serverIP, serverPort))
                break
            except Exception as e:
                e_f=1
                print ('error : '+ str(e))
                break
        if e_f==1:
            e_f=0
        else:
            for i in range(sensorNo):
                sen[i] = '"s'+str(i+1)+'":'+str(random.randint(1,21))   # Random number 1-20
            sen_data=''
            for i in range(sensorNo):
                sen_data=sen_data+sen[i]+','
            all_data='"'+'line'+str(line)+'":{"line":'+str(line)+','+ sen_data + '"ts":'+str(time.time())+'},'
            
            # all_data='%03$RD000030000389_' + str(n)
            # n=n+1
            print (all_data)
            clientSocket.send(all_data.encode('utf-8'))
            while 1:
                msg=clientSocket.recv(32)
                msg=msg.decode('ascii')
                # print (msg)
                # Get 'ack' from Socket Server
                if msg=='ack':
                    clientSocket.send('ok'.encode('utf-8'))
                    clientSocket.close()
                    break
                elif msg=='closed':
                    print ('Socket Server is closed')
                    clientSocket.close()
                    break
        print ('-----------------')
    except KeyboardInterrupt:
        break
    except Exception as e:
        print ('Error : '+ str(e))
        # break

print ("Connection is closed!")
clientSocket.send('ok'.encode('utf-8'))
## close the socket connection
clientSocket.close()

    
        


