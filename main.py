import db_connection as db_connection
from db_connection import create_connection
from flask import Flask, redirect, url_for, render_template, request, flash, session,jsonify
from flask_sqlalchemy import SQLAlchemy
<<<<<<< Updated upstream
from sqlalchemy import create_engine
from db_connection import load_salon_from_db
=======
>>>>>>> Stashed changes

webApp = Flask(__name__)

# Database connection function 
#db_connection.database_connection()


#Home page
@webApp.route('/')
def home():
        return render_template('home.html')

#Log In page
@webApp.route('/login')
def login():
    return render_template('login.html')

#Sing Up page
@webApp.route('/login_salon')
def login_salon():
    return render_template('login_salon.html')


#About page
@webApp.route('/about')
def about():
    return render_template('about.html')

#Contact page
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
#@webApp.route('/singin', methods=['GET' , 'POST'])
#def register():
    #pass

if __name__ == "__main__":
    webApp.run(debug=True)

