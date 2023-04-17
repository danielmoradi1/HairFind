from db_connection import database_connection, register_user
import psycopg2
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify


webApp = Flask(__name__)

# Database connection function
db_connection = database_connection()
cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


# Home page
@webApp.route('/')
def home():
    return render_template('home.html')


# Log In page for customer
@webApp.route('/login', methods=['GET', 'POST'])
def login_customer():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        try:
            cursor.execute(
                "SELECT * FROM user_table WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                password_re = user['password']
                if check_password_hash(password_re, request.form['password']):
                    # set session variables
                    session['loggedin'] = True
                    session['fullname'] = user['fullname']
                    session['username'] = user['username']
                    print(f"{username} Login Successfully")
                    # redirect to user profile page
                    return 'Welcome to the user profile'

            else:
                flash('Felaktigt användarnamn eller lösenord. Försök igen!')
                return render_template('login_customer.html')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Error occurred while logging in"

    else:
        return render_template('login_customer.html')


# Sign up page for customer
@webApp.route('/signup', methods=['GET', 'POST'])
def signUp():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        full_name = request.form['full_name']
        phone_number = request.form['phone_number']
        username = request.form['username']
        password = request.form['password']

        try:

            # Check if account already exists"select * from user_table where email = %s",

            cursor.execute(
                "SELECT * FROM user_table WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                flash('Username already exists. Please try a different username!')
                return render_template('login_customer.html')

            elif not full_name or not phone_number or not username or not password:
                flash('Please fill out the form!')
                return render_template('login_customer.html')

            else:
                hashed_password = generate_password_hash(
                    password, method='sha256')
                register_user(full_name, phone_number,
                            username, hashed_password)
                flash("Successfully created!")
                return redirect(url_for('login_customer'))

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Error occurred while signing up"
    else:
        return render_template('login_customer.html')


# Profile page
@webApp.route('/user_profile')
def user_profile():
    if 'loggedin' in session:
        return render_template('user_profile.html')
    else:
        return render_template('login_customer.html')


# define route for logout
@webApp.route('/logout')
def logout():
    # clear session variables and redirect to login page
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect('/login')


# Sing Up page
@webApp.route('/login_salon')
def login_salon():
    return render_template('login_salon.html')


# About page
@webApp.route('/about')
def about():
    return render_template('about.html')

# Contact page


@webApp.route('/contactUs')
def contactUs():
    return render_template('contactUs.html')


"""
conn = create_connection()
#Define  a dynamic route
@webApp.route('/salon/<int:org_number>')
def display_salon(org_number):
    salon = load_salon_from_db(org_number)
    if not salon:
        return "Not Found", 404
    return render_template('salon.html', salon= salon)
"""
# @webApp.route('/singin', methods=['GET' , 'POST'])
# def register():
# pass

if __name__ == "__main__":
    webApp.secret_key = secrets.token_hex(16)
    webApp.run(debug=True)
    