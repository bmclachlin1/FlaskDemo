from flask import Flask, redirect, url_for, render_template, request, session, flash
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
import sys

app = Flask(__name__)

app.secret_key = "Super secret key!!!"

# Connect to 'demo' DB as 'blake'
try:
  cnx = mysql.connector.connect(user='blake', password='password', host='127.0.0.1', database = 'demo')
  cnx.autocommit = True
  cursor = cnx.cursor(dictionary=True)
  print("Successfully connected to demo!")
except mysql.connector.Error as err:
  print(f"Error: {err}")
  sys.exit(0)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    # An output message
    msg=''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # store username and password in variables for easy access
        username = request.form['username']
        password = request.form['password']

        # query the database for a user with username and password
        query = ('SELECT * FROM users WHERE username=%s AND password=%s')
        data_user = (username, password)
        cursor.execute(query, data_user)

        # grab record from database
        account = cursor.fetchone()

        # if account exists
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            
            # redirect the user to the user page
            return redirect(url_for('user'))
        # account does not exist
        else:
            msg='Incorrect username and/or password!'
    
    return render_template("login.html", msg=msg)

@app.route('/logout')
def logout():
    if "username" in session:
        user = session["username"]
        flash(f"You have been logged out, {user}", "info")
        session.pop("username", None)
        session['loggedin'] = False
    return redirect(url_for("home"))   

@app.route('/user')
def user():
    if "username" in session and session['loggedin'] == True:
        user = session["username"]
        return render_template("user.html", user=user)
    else:
        return redirect(url_for("login"))
        
if __name__ == '__main__':
    app.run(debug=True)