import socket
import sqlite3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket created')
port = 5534
s.bind(('', port))
print ('Socket binded to port')
s.listen(5)
print ('socket is listening')

conn = sqlite3.connect('cis427_crypto.sqlite')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS Users 
                        (
                        ID int NOT NULL, 
                        first_name varchar(255), 
                        last_name varchar(255), 
                        user_name varchar(255) NOT NULL, 
                        password varchar(255), 
                        usd_balance DOUBLE NOT NULL, 
                        PRIMARY KEY (ID) 
                        );""")

conn.commit()

c.execute("""create table if not exists Cryptos 
                        ( 
                        ID int NOT NULL AUTO_INCREMENT, 
                        crypto_name varchar(10) NOT NULL, 
                        crypto_balance DOUBLE, 
                        user_id int, 
                        PRIMARY KEY (ID), 
                        FOREIGN KEY (user_id) REFERENCES Users ID) 
                        );""")


while True:
    clt, adr = s.accept()
    print ('Got connection from ', adr)
    clt.send(bytes("Thank you for connecting", "utf-8"))
    clt.close()


while True:

        c, addr = server.accept() # Establish connection with client.
        print('Got connection from', addr)
        
        while True:
                
                command = c.recv(1024).decode()
                if command == 'BUY' or command == 'buy':
                        
                        
                        
                        c.send('BUY'.encode())
                        break
                else:
                        print()

                

        conn.close()

