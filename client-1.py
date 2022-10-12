import socket

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5534
c.connect(('127.0.0.1', port))
message = c.recv(1024)
print(message.decode("utf-8"))


while True:
        message = input("Commands-> BUY \n SELL \n BALANCE \n LIST \n SHUTDOWN \n QUIT \n\n ->")
        print(message)

        if(message == 'BUY'): 

                break


               


c.close()


