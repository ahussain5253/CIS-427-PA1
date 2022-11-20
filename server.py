# import threading
# import socket
import sqlite3

#Connect database
conn = sqlite3.connect('cis427_crypto.sqlite')
u = conn.cursor()

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
cur = u.execute("SELECT count(*) FROM Users")
for row in cur:
    if (row[0] == 0):
        #Insert default user
        u.execute("INSERT INTO Users (ID, first_name, last_name, user_name, password, usd_balance) VALUES (1, 'Default', 'User','DefUser','defu', 100);")

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

def create():
    
    id = input("\nEnter New User ID: \n\n")
    fname = input("\nEnter First Name: \n\n")
    lname = input("\nEnter Last Name: \n\n")
    uname = input("\nEnter New Username: \n\n")
    pswd = input("\nEnter New Password: \n\n")
    balance = input("\nEnter New Balance: \n\n")
    print('\nNew User ' + uname + ' has been added\n\n')
        
    u.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?)", (id, fname, lname, uname, pswd, balance))
    conn.commit()

def addFunds(amt,userID):
    
    for row in u.execute("SELECT usd_balance FROM Users WHERE ID = ?", (userID)):
        currAmt = row[0]
        break
    
    currAmt += amt
    
    u.execute("UPDATE Users SET usd_balance = ? WHERE ID = ?", (currAmt, userID))
    conn.commit()
    
    print("\n\nFunds added successfully\nNew Balance: $%.2f" % currAmt + "\n")

def buy(command, cryptoName, cryptoAmt, pricePerCrypto, userID):
    
    for row in u.execute("SELECT count(*) FROM Users WHERE ID = ?", userID):
        uidexists = row[0]

    #Checks if user id exists or not then prompts to make a new one
    if (uidexists == 0):
        createUID = input("\n\n400 user not found error\nUser ID not found\nMake new user? Type Y or N\n\n")
        
        if (createUID == 'y') or (createUID == 'Y'):
            create()
    else:            
        print('\nRecieved: ' + command + '\n' + '200 OK')
    
        amt = float(cryptoAmt)
        ppc = float(pricePerCrypto)
    
        price = amt * ppc
    
        #Update user balance in database
        for row in u.execute("SELECT usd_balance FROM Users WHERE ID = ?", (userID)):
            currAmt = row[0]
            break
        
        #Checks if the user has enough to pay for crypto by looking at their current balance
        if (currAmt < price):
            balError = input("\n\n409 balance error\nNot enough balance in account\nAdd funds? Type Y or N\n\n")
            
            if (balError == 'y') or (balError == 'Y'):
                
                amt = input("\nHow much do you want to add?\n\n")
                famt = float(amt)
                
                addFunds(famt, userID)            
            
        else:       
            currAmt -= price
    
            u.execute("UPDATE Users SET usd_balance = ? WHERE ID = ?", (currAmt, userID))
            conn.commit()
    
            #Checks if there is a record for the user id. If not, adds one
            curr = u.execute("SELECT count(*) FROM Cryptos WHERE user_id = ? AND crypto_name = ?", (userID, cryptoName))
            for row in curr:
                if (row[0] == 0):
                    u.execute("INSERT INTO Cryptos (crypto_name, crypto_balance, user_id) VALUES (?,?,?)", (cryptoName, cryptoAmt, userID))
                    conn.commit()
            
                    for row in u.execute("SELECT crypto_balance FROM Cryptos WHERE user_id = ? AND crypto_name = ?", (userID, cryptoName)):
                        cryptBal = row[0] 
                 
                        newBal = str(cryptBal)
                 
                        print("BOUGHT: New balance: " + newBal + " " + cryptoName + ". " + "USD balance $%.2f" % currAmt + "\n") 
                        break 
            
            
                else:
                    for row in u.execute("SELECT crypto_balance FROM Cryptos WHERE user_id = ? AND crypto_name = ?", (userID, cryptoName)):
                        cryptBal = row[0]
                
                        nAmt = float(cryptoAmt)
                        cryptBal += nAmt
                
                        u.execute("UPDATE Cryptos SET crypto_balance = ? WHERE user_id = ? AND crypto_name = ?", (cryptBal, userID, cryptoName))
                        conn.commit()
                
                        newBal = str(cryptBal)
    
                        print("BOUGHT: New balance: " + newBal + " " + cryptoName + ". " + "USD balance $%.2f" % currAmt + "\n")

                        break  
   
def sell(command, cryptoName, cryptoAmt, pricePerCrypto, userID):
    
    #Check if there is a user id record in the user table
    for row in u.execute("SELECT count(*) FROM Users WHERE ID = ?", userID):
        uidexistsUs = row[0]
    
    for row in u.execute("SELECT count(*) FROM Cryptos WHERE user_id = ?", userID):
        uidexistsCr = row[0]
            
    #Checks if user id exists or not then prompts to make a new one
    if (uidexistsUs == 0) :
        createUID = input("\n\n400 user not found error\nUser ID not found in Users\nMake new user? Type Y or N\n\n")
        
        if (createUID == 'y') or (createUID == 'Y'):
            create()
    else:   
        if (uidexistsCr == 0):
            buyCrypto = input("\n\n400 no crypto record for user error\nUser specified has never bought crypto and has no record\nWould you like to buy crypto? Type Y or N\n\n")
            
            if (buyCrypto == 'Y') or (buyCrypto == 'y'):
                cryptoName = input("\n\nType in the name of the crypto to buy\n\n")
                cryptoAmt = input("\n\nType in the amount of crypto to buy\n\n")
                pricePerCrypto = input("\n\nType in the price per each crypto\n\n")
                
                buy("BUY", cryptoName, cryptoAmt, pricePerCrypto, userID)
        else:
            for row in u.execute("SELECT count(*) FROM Cryptos WHERE crypto_name = ? AND user_id = ?", (cryptoName, userID)):
                crypuidExists = row[0]
            
            if (crypuidExists == 0):
                bCrypto = input("\n\n300 no crypto record found for user error\nCrypto specified has never been bought by user and has no record\nWould you like to buy some " + cryptoName + " crypto? Type Y or N\n\n")
                
                if (bCrypto == 'y') or (bCrypto == 'Y'):
                    cryptoAmt = input("\n\nType in the amount of "+ cryptoName +" to buy\n\n")
                    pricePerCrypto = input("\n\nType in the price per each "+ cryptoName +"\n\n")
                    
                    buy("BUY", cryptoName, cryptoAmt, pricePerCrypto, userID)
                
                else:         
                    print('\nRecieved: ' + command + '\n' + '200 OK')
    
                    amt = float(cryptoAmt)
                    ppc = float(pricePerCrypto)
    
                    price = amt * ppc
            
                    for row in u.execute("SELECT usd_balance FROM Users WHERE ID = ?", (userID)):
                        currAmt = row[0]
                        break
        
                    currAmt += price
    
                    u.execute("UPDATE Users SET usd_balance = ? WHERE ID = ?", (currAmt, userID))
                    conn.commit()
    
                    for row in u.execute("SELECT crypto_balance FROM Cryptos WHERE user_id = ? AND crypto_name = ?", (userID, cryptoName)):
                        cryptBal = row[0]
                
                        nAmt = float(cryptoAmt)
                        cryptBal -= nAmt
                
                        u.execute("UPDATE Cryptos SET crypto_balance = ? WHERE user_id = ? AND crypto_name = ?", (cryptBal, userID, cryptoName))
                        conn.commit()
                
                        newBal = str(cryptBal)
    
                        print("SOLD: New balance: " + newBal + " " + cryptoName + ". " + "USD balance $%.2f" % currAmt + "\n")

                        break 
       
       
def shutdown():
    exit()

while True:
    
    command = input("\nType in full command \n\n CREATE \n BUY \n SELL \n BALANCE \n LIST \n CUSTOM \n SHUTDOWN \n QUIT \n\n ->")

    splitcommand = command.split()
    
    if (splitcommand[0] == 'CREATE'):
                     
        create()
        
    if (splitcommand[0] == 'BUY'):
        
        name = splitcommand[1]
        amt = splitcommand[2]
        ppc = splitcommand[3]
        uid = splitcommand[4]
        
        buy(command, name, amt, ppc, uid)
           
    if (splitcommand[0] =='SELL'):
           
        name = splitcommand[1]
        amt = splitcommand[2]
        ppc = splitcommand[3]
        uid = splitcommand[4]
        
        sell(command, name, amt, ppc, uid)    
                
    if (splitcommand[0] == 'CUSTOM'):
        
        query = input("\nPlease type the query in SQL: \n\n")
        u.execute(query)
        print('\nQuery processed successfully\n')
    
    if (splitcommand[0] == 'SHUTDOWN'):
        
        print("\nServer shutting down... Have a great day!\n")        
        shutdown()
    
    

    tof = input("Would you like to do something else? Type Y or N \n\n")
    
    if (tof == 'N') or (tof == 'n'):
        print("\nServer shutting down... Have a great day!\n")        
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