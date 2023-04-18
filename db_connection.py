import psycopg2
import psycopg2.extras


def database_connection():
    # Information about the MAU database
    hostname = 'pgserver.mau.se'
    database_name = 'hairfind_db'
    usernames = 'al0791'
    password = 'os577w59'
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
            print('connection successfully!')
        return connection
    except Exception as error:
        print(error)


# Function to register_salon
def register_salon_to_DB(org_number, name, username, telephone, address, password):
    conn = None
    cur = None

    try:
        # Read database configuration
        conn = database_connection()
        cur = conn.cursor()

        insert_script = "INSERT INTO salon_user (org_number, name, username, telephone, address, password) VALUES(%s, %s, %s, %s, %s, %s)"
        insert_value = (org_number, name, username, telephone, address, password)
        cur.execute(insert_script, insert_value)

        # Commit the changes to the database
        conn.commit()
        print('user successfully registered')
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting data in the table", error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

#register_salon(12, "John Doe", "johndoe@example.se", "123-456-7890", "123 Main St", "password123")

# Reads data from the table salon_user in database


def display_table_data(salon_user):
    conn = None
    cur = None
    try:
        conn = database_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM salon_user")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except (Exception, psycopg2.databaseError) as error:
        print("Error while fetching data from the table salon_user", error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


#display_table_data("salon_user")
# Registers users into the database table "user_table"


def register_user(fullname, telephone, username, password):
    conn = None
    cur = None

    try:
        # Read database configuration
        # connection, cursor = database_connection()
        conn = database_connection()
        cur = conn.cursor()

        insert_script = "INSERT INTO user_table (fullname, telephone, username, password) VALUES(%s, %s, %s, %s)"
        insert_value = (fullname, telephone, username, password)

        cur.execute(insert_script, insert_value)

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

# register_user(145, "Alex","Dahlberg", "07294556621", "johndoe@example.se", "Alex223")


# Reads data from the table user_table in database
def display_table_data(user_table):
    conn = None
    cur = None
    try:
        conn = database_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_table")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except (Exception, psycopg2.databaseError) as error:
        print("Error while fetching data from user_table", error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# display_table_data ("user_table")


# Function to edit user data
def edit_user_data(username, new_first_name=None, new_last_name=None, new_telephone=None, new_password=None):
    conn = None
    cur = None
    try:
        conn = database_connection()
        cur = conn.cursor()

        update_script = 'Update user_table SET'
        updates = []
        if new_first_name:
            updates.append(f"first_name = '{new_first_name}'")
        if new_last_name:
            updates.append(f"last_name = '{new_last_name}'")
        if new_telephone:
            updates.append(f"telephone = '{new_telephone}'")
        if new_password:
            updates.append(f"password = ''{new_password}")
        if not updates:
            raise ValueError("At least one field must be updated")
        update_script += ",".join(updates)
        update_script += f"WHERE username = {username}"

        cur.execute(update_script)
        conn.commit()
        print("User data updated sucessfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("En error has occrured while updating user data in the user_table", error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()


# edit_user_data('Roma', 'Sheeran', '0739548372', 'roma.sheeran@outlook.com', 'Roma123')


# Function to delete a user
def delete_user(username):
    conn = None
    cur = None
    try:
        conn = database_connection()
        cur = conn.cursor()

        delete_script = f"DELETE FROM user_table WHERE username = {username}"
        cur.execute(delete_script)
        conn.commit()
        print("User deleted successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while deleting user form the table", error)
    finally:
        if conn is not None:
            conn.close()
            if cur is not None:
                cur.close()
# delete_user('johndoe@example.se')



def get_salon_data(org_number):
    conn = None
    cur = None

    try:
        conn = database_connection()
        cur = conn.cursor()
        cur= conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM salon_user WHERE id=%s"
        cur.execute(query, (org_number))
        row_data = cur.fetchone()
        conn.close()
        return row_data
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while loading a salon from the salon_user")
    finally:
        if conn is not None:
            conn.close()
            if cur is not None:
                cur.close()



