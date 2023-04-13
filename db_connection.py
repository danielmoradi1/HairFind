import psycopg2
import psycopg2.extras


def database_connection():
    # Information about the MAU database
    hostname = 'pgserver.mau.se'
    database_name = 'hairfind_db'
    usernames = 'al0791'
    password = 'aks4rzug'
    port_id = 5432
    connection = None

    try:
        with psycopg2.connect(
            database=database_name,
            user=usernames,
            password=password,
            host=hostname,
            port=port_id
        ) as connection:

            # Open a cursor
            # with connection.cursor() as cursor:
            #cur = connection.cursor()
            #with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            # Every transaction needs a commit to the database. If we use withClass no commit needed
            # connection.commit()
            print('connection successfully!')
        return connection
    except Exception as error:
        print(error)


#Function to register_salon
def register_salon(org_number, name, email, telephone, address, password):
    conn = None
    cur = None
    
    try:
        # Read database configuration
        #connection, cursor = database_connection()
        conn = database_connection()
        cur = conn.cursor()
        
        insert_script = "INSERT INTO salon_user (org_number, name, email, telephone, address, password) VALUES(%s, %s, %s, %s, %s, %s)"
        insert_value =  (org_number, name, email, telephone, address, password)
        cur.execute(insert_script,insert_value)

        # Commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting data in the table", error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

#register_salon(123456, "John Doe", "johndoe@example.com", "123-456-7890", "123 Main St", "password123")

#Reads data from the table salon_user in database
def display_table_data(salon_user):
    conn =None
    cur = None
    try: 
        conn = database_connection()
        cur = conn.cursor()
        cur.execute ("SELECT * FROM salon_user")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except  (Exception, psycopg2.databaseError) as error:
        print("Error while fetching data from the table salon_user", error)
    finally: 
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
            print("Database connection is closed!")

display_table_data ("salon_user")

#Registers users into the database table "user_table"
def register_user(userId, firstName, lastName, telephone, emailId, password):
    conn = None
    cur = None
    
    try:
        # Read database configuration
        #connection, cursor = database_connection()
        conn = database_connection()
        cur = conn.cursor()
        
        insert_script = "INSERT INTO user_table (user_id, First_name, Last_name, telephone, Email_id, password) VALUES(%s, %s, %s, %s, %s, %s)"
        insert_value =  (userId, firstName, lastName, telephone, emailId, password)
        cur.execute(insert_script,insert_value)

        # Commit the changes to the database
        conn.commit()
        print("User inserted into the table")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting data in the table", error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

#register_user(145, "Alex","Dahlberg", "07294556621", "johndoe@example.se", "Alex223")


#Reads data from the table user_table in database
def display_table_data(user_table):
    conn =None
    cur = None
    try: 
        conn = database_connection()
        cur = conn.cursor()
        cur.execute ("SELECT * FROM user_table")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except  (Exception, psycopg2.databaseError) as error:
        print("Error while fetching data from user_table", error)
    finally: 
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
            print("Database connection is closed!")

display_table_data ("user_table")



