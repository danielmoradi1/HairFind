import db_connection as db_connection
from flask import Flask, redirect, url_for, render_template, request, flash, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

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

#@webApp.route('/singin', methods=['GET' , 'POST'])
#def register():
    #pass

if __name__ == "__main__":
    webApp.run(debug=True)
    

