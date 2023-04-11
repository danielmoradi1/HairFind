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
            with connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:

                create_scripts = (
                '''
                    CREATE TABLE IF NOT EXISTS user_table (
                    user_id serial PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    telephone VARCHAR(50) NOT NULL,
                    email_id VARCHAR(100) UNIQUE,
                    password VARCHAR(50) NOT NULL
                    );
                ''',

                '''
                    CREATE TABLE IF NOT EXISTS Salon_user(
	                org_number int PRIMARY KEY, 
	                SALON_NAME VARCHAR(50) NOT NULL,
	                email_id VARCHAR(100) UNIQUE,
	                telephone VARCHAR(50) NOT NULL,
	                address VARCHAR(200) NOT NULL,
	                description VARCHAR(400) NOT NULL,
	                password VARCHAR(50) NOT NULL
                    );
                ''',

                '''
                    CREATE TABLE IF NOT EXISTS SERVICE(
	                SERVIC_ID serial PRIMARY KEY,
                    salon_number int,
	                SERVIC_NAME VARCHAR(100) NOT NULL, 
	                PRICE INT NOT NULL,
	                DESCRIPTION VARCHAR(400) NOT NULL,
	                Image bytea,

                    FOREIGN KEY(salon_number) REFERENCES Salon_user(org_number)
                    );
                ''',

                '''
                    CREATE TABLE IF NOT EXISTS BOOKING(
                    User_id serial NOT NULL,
                    SERVIC_ID serial NOT NULL,
                    order_date DATE,
                    order_time DATE,

                    FOREIGN KEY(User_id) REFERENCES user_table(user_id),
                    FOREIGN KEY(SERVIC_ID) REFERENCES SERVICE(SERVIC_ID)
                    );
                '''
)


                for script in create_scripts:
                    cursor.execute(script)
            # Every transaction needs a commit to the database. If we use withClass no commit needed
            #connection.commit()
            print('connection successfully!')
    except Exception as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()
