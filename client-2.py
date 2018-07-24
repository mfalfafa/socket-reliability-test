# Socket Test Program

from socket import *

## Client Socket Communication initialization
serverIP = '169.254.148.241'    # PC Server IP
serverPort = 5002               # PC Server Port

n=0
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
                print ('error : '+ str(e))
        all_data='%01$RD000030000389_' + str(n)
        n=n+1
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
        break

print ("Connection is closed!")
clientSocket.send('ok'.encode('utf-8'))
## close the socket connection
clientSocket.close()

    
        


