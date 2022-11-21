import socket
import threading
import sqlite3

PORT = 5534

#Connect database
conn = sqlite3.connect('cis427_crypto.sqlite')
u = conn.cursor()

#Creating Socket
server = socket.socket()
print('Socket succesfully created')

server.bind(('', PORT))
print(f'socket binded to port{PORT}')

#Socket is awaiting response from client
server.listen()
           
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
        print('\nRecieved: ' + command + '\n')

        c.send("200 OK".encode())
    
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
                bCrypto = input("\n\n400 no crypto record found for user error\nCrypto specified has never been bought by user and has no record\nWould you like to buy some " + cryptoName + " crypto? Type Y or N\n\n")
                
                if (bCrypto == 'y') or (bCrypto == 'Y'):
                    cryptoAmt = input("\n\nType in the amount of "+ cryptoName +" to buy\n\n")
                    pricePerCrypto = input("\n\nType in the price per each "+ cryptoName +"\n\n")
                    
                    buy("BUY", cryptoName, cryptoAmt, pricePerCrypto, userID)
                
            else:
                for row in u.execute("SELECT crypto_balance FROM Cryptos WHERE crypto_name = ? AND user_id = ?", (cryptoName, userID)):
                    cBal = row[0]
                
                uamt = float(cryptoAmt)

                if (uamt > cBal):
                    byCrypto = input("\n\n400 not enough crypto to sell error\nUser ID #"+ userID +" does not have enough " + cryptoName + " in their balance to sell\nWould you like to buy more " + cryptoName + "? Type Y or N\n\n")

                    if (byCrypto == 'y') or (byCrypto == 'Y'):
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
       
def balance(user_id):
    for row in u.execute("SELECT count(*) FROM Users WHERE ID = ?", (user_id)):
        uidex = row[0]

    if (uidex == 0):
        createUser = input("\n\n400 user not found error\nUser ID not found\nMake new user? Type Y or N\n\n")    

        if (createUser == 'y') or (createUser == 'Y'):    
            create()
   
    else:
        print("\n\nRecieved: BALANCE\n200 OK")

        for row in u.execute("SELECT usd_balance FROM Users WHERE ID = ?", (user_id)):
            cbal = row[0]
        
        for row in u.execute("SELECT first_name FROM Users WHERE ID = ?", (user_id)):
            fname = row[0]

        for row in u.execute("SELECT last_name FROM Users WHERE ID = ?", (user_id)):
            lname = row[0]
        
        currbal = str(cbal)

        print("\n\nBalance for user " + fname + " " + lname + ": $%.2f" % cbal)
        print("\n\n")

def list(user_id):

    for row in u.execute("SELECT count(*)FROM Cryptos WHERE user_id = ?", (user_id)):
        uidex = row[0]
    
    if (uidex == 0):
        muser = input("\n\n400 no such user found in Cryptos error\nUser ID specified not found in Crytpos\nWould you like to purchase crypto? Type Y or N\n\n")

        if (muser == 'y') or (muser == 'Y'):
            cryptoName = input("\n\nType in the name of the crypto to buy\n\n")
            cryptoAmt = input("\n\nType in the amount of crypto to buy\n\n")
            pricePerCrypto = input("\n\nType in the price per each crypto\n\n")
                
            buy("BUY", cryptoName, cryptoAmt, pricePerCrypto, user_id)

    else:
        print("\n\nRecieved: LIST\n200 OK\nThe list of records in the Crypto database for user " + user_id + ":\n")

        num = 1

        records = u.execute("SELECT crypto_name, crypto_balance, user_id FROM Cryptos WHERE user_id = ?", (user_id))
        for row in records:

            print(str(num) + "  " + row[0] + " " + str(row[1]) + " " + str(row[2]))

            num += 1
        
        print("\n")

def shutdown():
    exit()

def quit():
    print("quit")


while True: 
    c, addr = server.accept()
    print('Got connection from', addr)

    command = c.recv(1024).decode()
    splitcommand = command.split()

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

    if (splitcommand[0] == 'BALANCE'):
        uid = input("\n\nEnter the User ID you want to see the balance for: \n\n")

        balance(uid)

    if (splitcommand[0] == 'LIST'):
        uid = input("\n\nEnter the User ID you want to list all records for: \n\n")

        list(uid)
    
    if (splitcommand[0] == 'CUSTOM'):
        
        query = input("\nPlease type the query in SQL: \n\n")
        u.execute(query)
        print('\nQuery processed successfully\n')
    
    if (splitcommand[0] == 'SHUTDOWN'):
        
        print("\nServer shutting down... Have a great day!\n")        
        shutdown()
    
    if (splitcommand[0] == 'QUIT'):

        quit()