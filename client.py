import socket
import threading

PORT = 5534

sock = socket.socket()
sock.connect(('127.0.0.1', PORT))
print("Connected to Server")
    
while True:
    
    command = input("\nType in full command \n\n BUY \n SELL \n BALANCE \n LIST \n CUSTOM \n SHUTDOWN \n QUIT \n\n ->")
    print("\n")

    sock.send(bytes(command,'utf-8'))

    while True:
        
        message = sock.recv(1024)
        
        if (message == "STOP".encode()):
            break
        elif (message ==  "QUIT".encode()):
            print("\nQUIT\n200 OK\n")
            exit()
        elif(message == "SHUTDOWN".encode()):
            print("\n200 OK\n")
            exit()
        else:
            print(message)
               



