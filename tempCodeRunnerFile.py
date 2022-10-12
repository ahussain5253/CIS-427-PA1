c.execute("""CREATE TABLE IF NOT EXISTS Users
                        (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name varchar(255), 
                        last_name varchar(255), 
                        user_name varchar(255) NOT NULL, 
                        password varchar(255)
                        );""")