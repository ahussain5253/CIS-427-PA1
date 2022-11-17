import socket
s = socket.socket()
port = 56789
s.connect(('127.0.0.1', port))
print("Connected to Server")
    
while True:
    
    fullcommand = input("\nType in full command \n\n BUY \n SELL \n BALANCE \n LIST \n SHUTDOWN \n QUIT \n\n ->")

    s.send(bytes(fullcommand,'utf-8'))

    print(s.recv(1024))


