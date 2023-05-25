from db_connection import *
import psycopg2
import secrets
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import flash
from flask import session
from flask_mail import Mail
from flask_mail import Message
from functools import wraps
from wtforms import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import validators


webApp = Flask(__name__)
# Database connection function
db_connection = database_connection()
cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Mail connection
webApp.config['MAIL_SERVER'] = 'smtp.gmail.com'
webApp.config['MAIL_PORT'] = 465
webApp.config['MAIL_USE_SSL'] = True
webApp.config['MAIL_USE_TLS'] = False
webApp.config['MAIL_USERNAME'] = 'service.hairfind@gmail.com'
webApp.config['MAIL_PASSWORD'] = 'tynjvdeipkqpykgr'
mail = Mail(webApp)


def send_new_password(email, new_password):
    """
        Arg:
            email, new_password
            The send_new_password() tags two parameters:
            The user email and user new password.
            Email = username
            Then it sends the new password to the user email with an email body
    """
    msg = Message("Nytt lösenord från HairFind",
                  sender="service.hairfind@gmail.com")
    msg.recipients = [email]
    msg.body = f'Hej {email}\nHAIRFIND \nDitt nya lösenord är: {new_password}'
    mail.send(msg)


# Welcome message function
def send_welcome_email(name, email):
    """
        Arg:
            name, email
            The send_welcome_email() tags two parameters:
            The user name and user email.
            Email = username
            Then it sends a welcome text to the user
    """
    msg = Message("Välkommen till HairFind",
                  sender="service.hairfind@gmail.com")
    msg.recipients = [email]
    msg.body = f'HAIRFIND \nHej {name} \nVälkomen till vårtjänst \nVi är glada att ha dig som kund!'
    mail.send(msg)


def delete_confirmation(username):
    msg = Message("Raderat konto", sender="service.hairfind@gmail.com")
    msg.recipients = [username]
    msg.body = f'HAIRFIND \nDitt konto {username} har raderats nu.\nDu är välkomen tillbaka!'
    mail.send(msg)


# Home page
@webApp.route('/')
def home():
    cursor.execute(
        "SELECT org_number, name, address, telephone FROM salon_user")
    salon_data = cursor.fetchall()
    return render_template('home.html', salon_data=salon_data)


############################
####    User functions #####
############################

# Log In page for customer

@webApp.route('/login_customer', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'].lower()
        password = request.form['password'].lower()
        print(password)

        try:
            cursor.execute(
                "SELECT * FROM user_table WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user is not None:
                hashed_password = user['password']
                print(hashed_password)
                if check_password_hash(hashed_password, password):
                    # set session variables
                    session['loggedin'] = True
                    session['fullname'] = user['fullname']
                    session['username'] = user['username']
                    print(f"{username} Login Successfully")
                    # redirect to user profile page
                    return redirect(url_for('customer_profile', username=username))
                else:
                    flash(
                        'Felaktigt användarnamn eller lösenord. Försök igen!', 'warning')
                    return render_template('login_customer.html')

            elif not user or not check_password_hash:
                flash('Vänligen fyll i formuläret!', 'info')
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
        full_name = request.form['full_name'].lower()
        phone_number = request.form['phone_number'].lower()
        username = request.form['username'].lower()
        password = request.form['password'].lower()

        try:
            # Check if account already exists
            cursor.execute(
                "SELECT * FROM user_table WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                flash(
                    'Username already exists. Please try a different username!', 'info')
                return render_template('register_customer.html')

            else:
                if not full_name or not phone_number or not username or not password:
                    flash('Vänligen fyll i formuläret!', 'info')
                    return render_template('register_customer.html')

                elif len(password) >= 4:
                    hashed_password = generate_password_hash(
                        password, method='sha256')
                    register_user(full_name, phone_number,
                                  username, hashed_password)
                    flash('Ditt konto har skapats!', 'success')
                    send_welcome_email(full_name, username)
                    return redirect(url_for('register_customer'))
                else:
                    flash('Vänligen ange lösenord större än 4 siffror!', 'info')
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
        cursor.execute(
            "SELECT fullname, telephone FROM user_table WHERE username = %s", (username,))
        user_info = cursor.fetchall()
        print(user_info)
        fullname = user_info[0][0]
        telephone = user_info[0][1]
        return render_template('customer_profile.html', username=username, fullname=fullname, telephone=telephone)
    else:
        return render_template('login_customer.html')


# Delete user account
@webApp.route('/delete_user/<username>', methods=['GET'])
def delete_user_account(username):
    if 'loggedin' in session:
        delete_user(username)
        delete_confirmation(username)
        return redirect(url_for('logout'))
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
                    session['username'] = username
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
            # Check if account already exists
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


# Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('salon_login'))
    return wrap


# Salon dashboard
@webApp.route('/salon_dashboard')
@is_logged_in
def salon_dashboard():
    username = session['username']
    cursor.execute(
        "SELECT NAME FROM Salon_user WHERE username = %s", (username,))
    user_info = cursor.fetchone()

    if user_info:
        fullname = user_info[0]
        cursor.execute(
            "SELECT * FROM service WHERE salon_username = %s", (username,))
        services = cursor.fetchall()

        return render_template('salon_dashboard.html', services=services, fullname=fullname)

    return render_template('salon_login.html')


# Service Form Class
class ArticleForm(Form):
    name = StringField('Tjänstnamn', [validators.Length(min=1, max=50)])
    price = StringField('Pris', [validators.Length(min=1, max=10)])
    description = TextAreaField(
        'Beskrivning', [validators.Length(min=10, max=200)])


# Add Service
@webApp.route('/add_service', methods=['GET', 'POST'])
@is_logged_in
def add_service():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        price = int(form.price.data)  # Convert price to an integer
        description = form.description.data

        try:
            # Check if ID exists
            cursor.execute("SELECT EXISTS(SELECT 1 FROM service)")
            id_exists = cursor.fetchone()[0]

            # Get the last ID or start from 1
            if id_exists:
                cursor.execute("SELECT MAX(service_id) FROM service")
                last_id = cursor.fetchone()[0]
                service_id = last_id + 1
            else:
                service_id = 1

            # Execute the action
            insert_script = "INSERT INTO service (service_id, service_name, price, description, salon_username) VALUES(%s, %s, %s, %s, %s)"
            insert_value = (service_id, name, price,
                            description, session['username'])
            cursor.execute(insert_script, insert_value)

            db_connection.commit()
            flash('Tjänsten är klar!', 'success')
            return redirect(url_for('salon_dashboard'))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            flash('Ett fel inträffade. Försök igen senare', 'error')
    return render_template('add_service.html', form=form)


@webApp.route('/edit_service/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_service(id):
    # Get service by id
    cursor.execute("SELECT * FROM service WHERE service_id = %s", [id])
    service = cursor.fetchone()

    if service is not None:

        # Get form
        form = ArticleForm(request.form)

        # Populate service form fields
        form.name.data = service[1]
        form.price.data = str(service[2])
        form.description.data = service[3]

        if request.method == 'POST' and form.validate():
            name = request.form['name']
            price = request.form['price']
            description = request.form['description']

            # Execute
            cursor.execute(
                "UPDATE service SET service_name=%s, price=%s, description=%s WHERE service_id=%s", (name, price, description, id))
            # Commit to DB
            db_connection.commit()
            flash('Ändringar är klara!', 'success')
            return redirect(url_for('salon_dashboard'))
    else:
        flash('Service not found', 'error')
        return redirect(url_for('salon_dashboard'))
    return render_template('edit_service.html', form=form)


# Delete service
@webApp.route('/delete_service/<string:id>', methods=['POST'])
@is_logged_in
def delete_service(id):
    # Execute
    cursor.execute("DELETE FROM service WHERE service_id = %s", [id])
    # Commit to DB
    db_connection.commit()
    flash('Tjänsten har tagits bort!', 'success')
    return redirect(url_for('salon_dashboard'))


# Reset password function for both salon and user accounts
@webApp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        new_password = request.form['password']
        try:
            # Check if the salon user already has in the database
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


# Log out function
@webApp.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Ditt är Utloggad nu!', 'success')
    # session.pop('loggedin', None)
    # session.pop('username', None)
    return redirect(url_for('login_customer'))


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


@webApp.route('/salon/<int:salon_id>')
def salon_page(salon_id):
    salon_data = get_salon_data(salon_id)
    if not salon_data:
        return "Salon not found"

    username = salon_data[1]
    service_info = get_service_info(username)

    return render_template('salon.html', salon_data=salon_data, service_info=service_info)

@webApp.route('/search')
def search():
    query = request.args.get('query') #Get the search query from the request arguments
    service = request.args.get('service_name')
    price_range = request.args.get('price')
    description = request.args.get('description')
    salon_name = request.args.get('name')
    salon_address = request.args.get('address')
    salon_contact = request.args.get('telephone')


    # Construct 
    sql_query = "SELECT * FROM SERVICES_LIST WHERE NAME ILIKE '%{}%'".format(query)

    if service:
        sql_query += "AND service = '{}'".format(service)
    
    if price_range:
        min_price, max_price = price_range.splite('-')
        sql_query += "AND price >= {} AND price <= {}".format(min_price, max_price)

    if description:
        sql_query += "AND description = '{}'".format(description)

    if salon_name:
        sql_query += "AND name = '{}'".format(salon_name)
    
    if salon_address:
        sql_query += "AND address = '{}'".format(salon_address)

    if salon_contact: 
        sql_query += "AND telephone = '{}'".format(salon_contact)


    cursor.execute(sql_query)
    results = cursor.fetchall()

    
    return render_template('Results.html', results=results)

if __name__ == "__main__":
    webApp.secret_key = secrets.token_hex(16)
    webApp.run(debug=True)
