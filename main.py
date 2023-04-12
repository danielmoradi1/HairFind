import psycopg2
from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask import templating

# Database connection function
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
            # Execute the script to the database
            # cursor.execute()
            # Every transaction needs a commit to the database. If we use withClass no commit needed
            print('connection successfully!')
    except Exception as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()
        
#database_connection()


webApp = Flask(__name__)
webApp.config['SQLALCHEMY_DATABASE_URi'] = 'postgresql://po'
#database = SQLAlchemy(webApp)

@webApp.route('/')
def hello():
    return render_template('home.html')

@webApp.route('/signIn')
def SignIn():
    return render_template('signIn.html')

@webApp.route('/contactUs')
def contactUs():
    return render_template ('contactUs.html')

@webApp.route('/about')
def about():
    return render_template ('about.html')

@webApp.route('/signIn', methods=['GET'])
def signIn():
    print('New page accessed.')
    return render_template('SignIn.html')

if __name__ == "__main__":
    webApp.run(debug=True)
