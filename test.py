import sqlite3

conn = sqlite3.connect('cis427_crypto.sqlite')

print("Opened database successfully")

conn.execute('''CREATE TABLE IF NOT EXISTS COMPANY
                   (ID INT PRIMARY KEY NOT NULL,
                   NAME TEXT NOT NULL,
                   AGE INT NOT NULL,
                   ADDRESS CHAR(50),
                   SALARY REAL);''')

# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (1, 'Paul', 32, 'California', 20000.00 )")

# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")

# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")

# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
# conn.commit()
# print("Records created successfully")



# cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
# for row in cursor:
#    print ("ID = ", row[0])
#    print ("NAME = ", row[1])
#    print ("ADDRESS = ", row[2])
#    print ("SALARY = ", row[3], "\n")
   
# print ("Operation done successfully")

def updateTable(ID,Salary):
    conn.execute("UPDATE COMPANY set SALARY = ? where ID = ?", (Salary, ID))
    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)

    print ("Operation done successfully")


# conn.execute("DELETE from COMPANY where ID = 12;")
# conn.commit()
# print ("Total number of rows deleted :", conn.total_changes)

# cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
# for row in cursor:
#    print ("ID = ", row[0])
#    print ("NAME = ", row[1])
#    print ("ADDRESS = ", row[2])
#    print ("SALARY = ", row[3], "\n")

# print ("Operation done successfully")

id = input("Type ID# \n")
sal = input("Type salary \n")

updateTable(id,sal)


conn.close()