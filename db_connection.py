import psycopg2
import psycopg2.extras

# Database connection function


def database_connection():
    """
        The database_connection() function connects to the MAU database
        it opens the database connection and prints the ('connection successfully')
        return connection
    """

# https://pgserver.mau.se:6502/kill.html
    # Information about the MAU database
    hostname = 'pgserver.mau.se'
    database_name = 'hairfind_db'
    username = 'al0791'
    password = 'os577w59'
    port_id = 5432
    connection = None

    try:
        with psycopg2.connect(
            database=database_name,
            user=username,
            password=password,
            host=hostname,
            port=port_id
        ) as connection:
            print('connection successfully!')
        return connection
    except Exception as error:
        print(error)


# local variables for database connection
# local variables for cursor
db_connection = database_connection()
cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Function to register_salon


def register_salon_to_DB(org_number, name, username, telephone, address, password):
    """
        Arg:
        The function takes the following parameters:
        org_number, name, username, telephone, address, password
        The register_salon_to_DB() register salon to the database
    """

    conn = None
    cur = None

    try:
        # Read database configuration
        conn = database_connection()
        cur = conn.cursor()

        insert_script = "INSERT INTO salon_user (org_number, name, username, telephone, address, password) VALUES(%s, %s, %s, %s, %s, %s)"
        insert_value = (org_number, name, username,
                        telephone, address, password)
        cur.execute(insert_script, insert_value)

        # Commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting data in the table", error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()


def display_table_data(salon_user):
    """
        Arg:
        The function takes the following parameter:
        salon_user
    """

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

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting data in the table", error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()


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
    except (Exception, psycopg2.DatabaseError) as error:
        print("En error has occrured while updating user data in the user_table", error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()


# Function to delete a user
def delete_user(username):
    conn = None
    cur = None
    try:
        conn = database_connection()
        cur = conn.cursor()
        delete_script = f"DELETE FROM user_table WHERE username = '{username}'"
        cur.execute(delete_script)
        conn.commit()
        print('User deleted successfully!')
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while deleting user from the table:", error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def get_salon_data(salon_id):
    cursor.execute(
        "SELECT name, username, telephone, address FROM salon_user WHERE org_number = %s", (salon_id,))
    salon_data = cursor.fetchone()

    if not salon_data:
        # Handle case where salon ID is not found
        return None
    salon_data = {
        'name': salon_data[0],
        'username': salon_data[1],
        'telephone': salon_data[2],
        'address': salon_data[3]
    }
    return salon_data



def get_service_info(username):
    cursor.execute(
        "SELECT service_name, price, description FROM service WHERE salon_username = %s", (username,))
    service_info = cursor.fetchall()

    if not service_info:
        # Handle case where no services are found
        return None
    return service_info

result = get_service_info('daniel.moradi15@gmail.com')
print(result)

# Edit salon Information
def edit_salon_info(salon_id, name, phone_number, address):
    print('salon information!')
    
    try:
        cursor.execute(
            "UPDATE salon_user SET name=%s, telephone=%s, address=%s WHERE org_number=%s",
            (name, phone_number, address, salon_id))  # Updated column name
        # Commit to DB
        db_connection.commit()
        print(salon_id, name, phone_number, address)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
