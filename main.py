from db_connection import database_connection, register_user, register_salon_to_DB
import psycopg2
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, redirect, url_for, render_template, request, flash, session
from db_connection import get_salon_data
from flask_mail import Mail, Message

webApp = Flask(__name__)
# Database connection function
db_connection = database_connection()
cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

webApp = Flask(__name__)
# Mail connection
webApp.config['MAIL_SERVER'] = 'smtp.gmail.com'
webApp.config['MAIL_PORT'] = 465
webApp.config['MAIL_USE_SSL'] = True
webApp.config['MAIL_USE_TLS'] = False
webApp.config['MAIL_USERNAME'] = 'service.hairfind@gmail.com'
webApp.config['MAIL_PASSWORD'] = 'tynjvdeipkqpykgr'
mail = Mail(webApp)




# Function to send new password to user mail
def send_new_password(email, new_password):
    msg = Message("Nytt lösenord från HairFind", sender = "service.hairfind@gmail.com")
    msg.recipients = [email]
    msg.body = f'Hej {email}\nHAIRFIND \nDitt nya lösenord är: {new_password}'
    mail.send(msg)

#Welcome message function
def send_welcome_email(name, email):
    msg = Message("Välkommen till HairFind", sender="service.hairfind@gmail.com")
    msg.recipients = [email]
    msg.body = f'HAIRFIND \nHej {name} \nVälkomen till vårtjänst \nVi är glada att ha dig som kund!'
    mail.send(msg)


# Home page
@webApp.route('/')
def home():
    return render_template('home.html')


############################
####    User functions #####
############################

# Log In page for customer
@webApp.route('/login_customer', methods=['GET', 'POST'])
def login_customer():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)

        try:
            cursor.execute(
                "SELECT * FROM user_table WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                hashed_password = user['password']
                print(hashed_password)
                if check_password_hash(hashed_password, password):
                    # set session variables
                    session['loggedin'] = True
                    session['fullname'] = user['fullname']
                    session['username'] = user['username']
                    print(f"{username} Login Successfully")
                    # redirect to user profile page
                    flash("you are successfuly logged in")
                    return redirect(url_for('customer_profile', username=username))

                else:
                    flash(
                        'Felaktigt användarnamn eller lösenord. Försök igen!', 'warning')
                    return render_template('login_customer.html')

            else:
                flash('Please insert your email and password', 'error')
                return render_template('login_customer.html')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Error occurred while logging in"
    else:
        return render_template('login_customer.html')


# Sign up page for customer
@webApp.route('/register_customer', methods=['GET', 'POST'])
def register_customer():

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
                flash(
                    'Username already exists. Please try a different username!', 'info')
                return render_template('register_customer.html')

            else:
                if not full_name or not phone_number or not username or not password:
                    flash('Please fill out the form!', 'info')
                    return render_template('register_customer.html')

                elif len(password) >= 4:
                    hashed_password = generate_password_hash(
                        password, method='sha256')
                    register_user(full_name, phone_number,
                                  username, hashed_password)
                    flash('Your account has been created successfully!', 'success')
                    send_welcome_email(full_name, username)
                    return redirect(url_for('register_customer'))
                else:
                    flash('Please insert 4 characters', 'info')
                    return render_template('register_customer.html')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Error occurred while signing up"
    else:
        return render_template('register_customer.html')


# Profile page
@webApp.route('/customer_profile', )
def customer_profile():
    username = request.args.get('username')
    if 'loggedin' in session:
        return render_template('customer_profile.html', username=username)
    else:
        return render_template('login_customer.html')


# function to check if salon_user already exists
def user_exists(username):
    try:
        cursor.execute(
            "SELECT * FROM salon_user WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user is not None:
            return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return False


################################
####    Salon functions    #####
################################

# Log in salon account
@webApp.route('/salon_login', methods=['GET', 'POST'])
def salon_login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)

        try:
            cursor.execute(
                "SELECT * FROM salon_user WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user is not None:
                hashed_password = user['password']
                print(hashed_password)
                if check_password_hash(hashed_password, password):
                    # set session variables
                    session['loggedin'] = True
                    session['username'] = user['username']
                    print(f"{username} Login Successfully")
                    # redirect to user profile page
                    return redirect(url_for('salon_dashboard', username=username))

                else:
                    flash(
                        'Felaktigt användarnamn eller lösenord. Försök igen!', 'warning')
                    return render_template('salon_login.html')

            else:
                flash('Vänligen ange din e-postadress och ditt lösenord', 'error')
                # return render_template('salon_login.html')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Error occurred while logging in"

    return render_template('salon_login.html')


# Sign up salon account
@webApp.route('/register_salon', methods=['GET', 'POST'])
def register_salon():
    if request.method == 'POST' and 'org_number' in request.form and 'username' in request.form and 'password' in request.form:

        org_number = request.form['org_number']
        name = request.form['name']
        username = request.form['username']
        phone_number = request.form['phone_number']
        address = request.form['address']
        password = request.form['password']

        try:
            # Check if account already exists"select * from user_table where email = %s",
            cursor.execute(
                "SELECT * FROM salon_user WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                flash(
                    'Användarnamn existerar redan. Försök med ett annat användarnamn!', 'info')
                return render_template('register_salon.html')

            else:
                if not org_number or not name or not username or not username or not phone_number or not address:
                    flash('Vänligen fyll i formuläret!', 'info')
                    return render_template('register_salon.html')

                elif len(org_number) <= 5 or len(org_number) >= 11:
                    flash('Vänligen ange rätt organisationsnummer!', 'info')
                    return render_template('register_salon.html')

                elif len(password) >= 4:
                    hashed_password = generate_password_hash(
                        password, method='sha256')
                    register_salon_to_DB(
                        org_number, name, username, phone_number, address, hashed_password)
                    flash('Ditt konto har skapats!', 'success')
                    send_welcome_email(name, username)
                    return redirect(url_for('register_salon'))

                else:
                    flash('Vänligen ange lösenord större än 4 siffror!', 'info')
                    return render_template('register_salon.html')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Error occurred while signing up"
    else:
        return render_template('register_salon.html')


# Salon dashboard login
@webApp.route('/salon_dashboard')
def salon_dashboard():
    username = request.args.get('username')
    if 'loggedin' in session:
        return render_template('salon_dashboard.html', username=username)
    else:
        return render_template('salon_login.html')


# Salon logout
def salon_logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash("You are successfully logged out.", "success")
    return redirect(url_for('salon_login'))


# Reset password function for both salon and user accounts
@webApp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        new_password = request.form['password']
        try:
            # Check if the user already has in the database
            cursor.execute(
                "SELECT * FROM salon_user WHERE username = %s", (username,))
            salon = cursor.fetchone()

            cursor.execute(
                "SELECT * FROM user_table WHERE username = %s", (username,))
            user = cursor.fetchone()

            # reset password for the salon user or user
            if salon is not None:
                username = salon["username"]
                table = "salon_user"

            elif user is not None:
                username = user["username"]
                table = "user_table"
            else:
                flash('Felaktig användare!', 'warning')
                return redirect(url_for('reset_password'))

            hashed_password = generate_password_hash(new_password)
            if isinstance(hashed_password, bytes):
                hashed_password = hashed_password.decode('utf-8')

            cursor.execute(
                f"UPDATE {table} SET password = %s WHERE username = %s", (
                    hashed_password, username)
            )
            db_connection.commit()

            send_new_password(username, new_password)
            flash(
                'Ditt lösenord har återställts. Var god logga in med ditt nya lösenord.', 'success')
            return redirect(url_for('reset_password'))

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            flash('Ett fel inträffade. Försök igen senare', 'error')

    return render_template('reset_password.html')



# define route for logout
@webApp.route('/logout')
def logout():
    # clear session variables and redirect to login page
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect('/login')


################################
####    Content pages      #####
################################
# About page
@webApp.route('/about')
def about():
    return render_template('about.html')


# Contact page
@webApp.route('/contact_us')
def contact():
    return render_template('contact_us.html')


# Define  a dynamic route
@webApp.route('/salon/<int:org_number>')
def display_salon(org_number):
    row_data = get_salon_data(org_number)
    return render_template('salon.html', row_data=row_data)


if __name__ == "__main__":
    webApp.secret_key = secrets.token_hex(16)
    webApp.run(debug=True)
