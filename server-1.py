import socket

s = socket.socket()
print('socket created')
port = 56789
s.bind(('', port))
print ('Socket binded to port')
s.listen(5)
print ('socket is listening')

while True:
    c, addr = s.accept()
    print ('Got connection from ', addr)
    message = ('Thanks for connecting')
    c.send(message.encode())
    c.close()

conn = sqlite3.connect('cis427_crypto.sqlite')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS
                users(  
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                user_name TEXT NOT NULL,
                password TEXT,         
                usd_balance DOUBLE NOT NULL
                );""")

c.execute("""CREATE TABLE IF NOT EXISTS
                cryptos(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                crypto_name varchar(10) NOT NULL,
                crypto_balance DOUBLE,
                user_id TEXT, 
                FOREIGN KEY (user_id) REFERENCES {self.users_table_name}(ID)
                );""")

c.execute('''INSERT INTO users (email, fname, lname, username, password, balance)
                VALUES  ('johnsmith@umich.edu', 'John', 'Smith', 'johnsmith1', 'johnsmith12345', 100.00),
                        ('cooperkupp@umich.edu', 'Cooper', 'Kupp', 'cooperkupp2', 'cooperkupp12345', 100.0),
                        ('mattstafford@umich.edu', 'Matt', 'Stafford', 'mattstafford3', 'mattstafford12345', 100.00),
                        ('traviskelce@umich.edu', 'Travis', 'Kelce', 'traviskelce4', 'traviskelce12345', 100.00),
                        ('imammar@umich.edu', 'Abe', 'Ammar', 'abeammar5', 'abeammar12345', 100.00)''')

c.execute('''INSERT INTO crypto (id, cname, cbalance, user_id, key)
                VALUES  ('Bitcoin', 30.0, 1)''')

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

                


        conn.commit()
        conn.close()

