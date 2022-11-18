import threading
import socket
import sqlite3

#Creating Socket
s = socket.socket()
print('Socket succesfully created')

#Creating Port
port = 56789
s.bind(('', port))
print(f'socket binded to port{port}')

#Socket is awaiting response from client
s.listen(5)
print('Socket is listening')

#Connect database
conn = sqlite3.connect('cis427_crypto.sqlite')
u= conn.cursor()

#Create users table
u.execute("""CREATE TABLE IF NOT EXISTS Users
                        (  
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name varchar(255),
                        last_name varchar(255),
                        user_name varchar(255) NOT NULL,
                        password varchar(255),         
                        usd_balance DOUBLE NOT NULL
                );""")

#Insert default user
u.execute("INSERT INTO Users (first_name, last_name, user_name, password, usd_balance) VALUES ('First', 'User','fuser','first', 100);")
conn.commit()

#Create Cryptos table
u.execute("""CREATE TABLE IF NOT EXISTS Cryptos
                        (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        crypto_name varchar(10) NOT NULL,
                        crypto_balance DOUBLE,
                        user_id int, 
                        FOREIGN KEY (user_id) REFERENCES Users (ID)
                );""")

conn.commit()

def buyCommand(cryptoName, cryptoAmt, pricePerCrypto, userID, command):

    print('Recieved: ' + command)

    u.execute("INSERT INTO Cryptos VALUES (?,?,?,?)", (userID, cryptoName, cryptoAmt, userID))
    conn.commit()


def deleteCommand(table):
    u.execute("DROP TABLE ?", (table,))
    conn.commit()

while True: 
    c, addr = s.accept()
    print('Got connection from', addr)

    command = c.recv(1024).decode()
    splitcommand = command.split()

    if splitcommand[0] == 'BUY':
        name = splitcommand[1]
        camt = splitcommand[2]
        ppc = splitcommand[3]
        uid = splitcommand[4]

        buyCommand(name,camt,ppc,uid,command)

    elif splitcommand[0] == 'DELETE':
        
        
        table = input("Enter name: \n")
        deleteCommand(table)
        

    

message = ('Thank you for connecting')
s.send(message.encode())

print(c.recv(1024))
c.close()