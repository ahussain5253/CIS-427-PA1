from email import message
import socket
import sqlite3
from venv import create


# create a socket at SERVER side
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket Created')

PORT = 7563 #this is my ID

# bind host address and port together
s.bind(('',PORT))
print('Socket Binded to Port')

 # configure how many clients the server can listen
s.listen(1)
print("Socket is Listening")

conn = sqlite3.connect('cis427_crypto.sqlite')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS Users
                        (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name varchar(255), 
                        last_name varchar(255), 
                        user_name varchar(255) NOT NULL, 
                        password varchar(255),
                        usd_balance DOUBLE NOT NULL
                        );""")

# c.execute("""DROP TABLE Users""")

conn.commit()

c.execute("""CREATE TABLE IF NOT EXISTS Cryptos 
                        ( 
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        crypto_name varchar(10) NOT NULL, 
                        crypto_balance DOUBLE, 
                        user_id int, 
                        FOREIGN KEY (user_id) REFERENCES Users (ID) 
                        );""")



while True:
    clt, adr = s.accept()
    print ('Got connection from ', adr)
    clt.send(bytes("Thank you for connecting", "utf-8"))
    clt.close()


while True:


        # def buy_command():



        def sell_command():
                usd_balance = float(crypto_q) * float(usd_price)
                crypto_balance = str(float(crypto_balance) - float(crypto_q))



        def getBalance():
                message_back_balance = ""



        # def getlist():







while True:

        c, addr = s.accept() # Establish connection with client.
        print('Got connection from', addr)

        while True:
                print("Waiting for Command")
                message_recieved = c.recv(1024).decode()
                commands = message_recieved.split("")

                if message_recieved == 'QUIT' or message_recieved == 'quit':
                        c.send("Quitting Client!")
                        break

                # elif message_recieved == 'BUY' or message_recieved == 'buy':
                #         message_back =

                # elif message_recieved == 'SELL' or message_recieved == 'sell':
                #         message_back =

                # elif message_recieved == 'LIST' or message_recieved == 'list':
                #         message_back =
                #         c.send(("200 OK \n")).encode()

                # elif message_recieved == 'BALANCE' or message_recieved == 'balance':
                #         message_back =
                #         c.send(("200 OK \n")).encode()

                # elif message_recieved == 'SHUTDOWN' or message_recieved == 'shutdown':
                #         c.send("Shutting Down!").encode()
                #         c.send(("200 OK \n")).encode()
                #         break


        conn.close()
