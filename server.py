# import threading
# import socket
from decimal import Decimal
import sqlite3

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

#Check if Users is empty
isEmpty = u.execute("SELECT count(*) FROM Users")

#Insert default user
if (isEmpty == 0):
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

def buy(command, cryptoName, cryptoAmt, pricePerCrypto, userID):

    print('\nRecieved: ' + command + '\n')
    
    amt = float(cryptoAmt)
    ppc = float(pricePerCrypto)
    
    price = amt * ppc
    
    print('Total Price: ', price)  
    print('\n')

    # u.execute("INSERT INTO Cryptos VALUES (?,?,?,?)", (userID, cryptoName, cryptoAmt, userID))
    # conn.commit()

def shutdown():
    
    exit()





def delete(table):
       
    if (table == 'U'):
        u.execute("DROP TABLE Users")
    elif (table == 'C'):
        u.execute("DROP TABLE Cryptos")


while True:
    
    fullcommand = input("\nType in full command \n\n BUY \n SELL \n BALANCE \n LIST \n SHUTDOWN \n QUIT \n DELETE \n\n ->")

    splitcommand = fullcommand.split()
    
    if (splitcommand[0] == 'BUY'):
        
        name = splitcommand[1]
        amt = splitcommand[2]
        ppc = splitcommand[3]
        uid = splitcommand[4]
        
        buy(fullcommand, name, amt, ppc, uid)
    
    if (splitcommand[0] == 'SHUTDOWN'):
        
        print("Server shutting down... Have a great day!")        
        shutdown()
    
    
    
    
    
    if (splitcommand[0] == 'DELETE'):
        
        table = input("Which table to delete? Type U (User) or C (Cryptos)")
        
        delete(table)
    
    
    tof = input("Would you like to do something else? Type Y or N \n\n")
    
    if (tof == 'N' or 'n'):
        
        print("\nServer shutting down... Have a great day!")        
        shutdown()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#Creating Socket
# s = socket.socket()
# print('Socket succesfully created')

# #Creating Port
# port = 56789
# s.bind(('', port))
# print(f'socket binded to port{port}')

# #Socket is awaiting response from client
# s.listen(5)
# print('Socket is listening')

# while True: 
#     c, addr = s.accept()
#     print('Got connection from', addr)

#     command = c.recv(1024).decode()
#     splitcommand = command.split()

#     if splitcommand[0] == 'BUY':
#         name = splitcommand[1]
#         camt = splitcommand[2]
#         ppc = splitcommand[3]
#         uid = splitcommand[4]

#         buyCommand(name,camt,ppc,uid,command)

#     elif splitcommand[0] == 'DELETE':
        
        
#         table = input("Enter name: \n")
#         deleteCommand(table)
        

    

# message = ('Thank you for connecting')
# s.send(message.encode())

# print(c.recv(1024))
# c.close()