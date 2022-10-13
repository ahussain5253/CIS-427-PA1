import socket
import sys


# Server name and Port number
HOST = '127.0.0.1'
PORT = 7563

# create a socket at CLIENT side
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT)) #connecting to host and port
msg = ("CONNECTED") #printing message CONNECTED
print(msg) #PRINT

while True:
        #TAKING INPUT OF USER
        message = input("Commands-> BUY \n SELL \n BALANCE \n LIST \n SHUTDOWN \n QUIT \n\n ->") 
        client_socket.send(message.encode())
        
        result = client_socket.recv(1024)

        #If result of message is quit or shutdown, then disconnect from server
        if(result == 'QUIT' or 'SHUTDOWN'): 
                print("Closing Client Connection! Goodbye!")
                break

#disconnect the client
client_socket.close()