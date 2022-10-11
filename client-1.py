import socket

c = socket.socket()
port = 56789
c.connect(('127.0.0.1', port))
print(c.recv(1024))   
c.close()

while True:
        message = input("Commands-> BUY \n SELL \n BALANCE \n LIST \n SHUTDOWN \n QUIT \n\n ->")
        print(message)
        if(message == 'QUIT' or 'SHUTDOWN'): 
                print("Closing Client Connection! Goodbye!")
                break
        elif(message == 'BUY'):
                print("test")

        # elif(result == 'SELL'):
                

        # elif(result == 'BALANCE'):
               

        # elif(result == 'LIST'):

               


c.close()


