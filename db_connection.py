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
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                pass
            # Every transaction needs a commit to the database. If we use withClass no commit needed
            # connection.commit()
        print('connection successfully!')
        return connection, cursor
    except Exception as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()


def register_salon(salonId, salonName, email, address, password):
    connection = None
    try:
        # Read database configuration
        connection, cursor = database_connection()

        # Execute the INSERT statement
        cursor.execute("INSERT INTO salon_user\
                    (org_number,name,email,telephone,address,password)" + 
                    "VALUES(%s,%s,%s,%s,%s)",
                    (salonId, salonName, email, address, password))
        
            # Commit the changes to the database
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting data in the table", error)
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()

register_salon(1223, 'MOMO', 'momo@malmo.se', 'Malmögatan1', '0000')