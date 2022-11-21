import socket
import threading

alias = input('Choose a name: ')
PORT = 5534

sock = socket.socket()
sock.connect(('127.0.0.1', PORT))
print("Connected to Server")
    
while True:
    
    command = input("\nType in full command \n\n BUY \n SELL \n BALANCE \n LIST \n CUSTOM \n SHUTDOWN \n QUIT \n\n ->")
    print("\n")

    sock.send(bytes(command,'utf-8'))

    print(sock.recv(1024))

    tof = input("\nWould you like to do something else? Type Y or N \n\n")
    
    if (tof == 'N') or (tof == 'n'):
        print("\nServer shutting down... Have a great day!\n")
        sock.close()   
        break     



