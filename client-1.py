import socket

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5534
c.connect(('127.0.0.1', port))
message = c.recv(1024)
print(message.decode("utf-8"))
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


