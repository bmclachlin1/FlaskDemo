from flask import Flask, redirect, url_for, render_template, request
from markupsafe import escape
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        return redirect(url_for("show_user", name=user))
    else:
        return render_template("login.html")

@app.route('/users')
def show_all_users():
    return 'All Users'

@app.route('/users/<name>')
def show_user(name):
    return f"<h1>{name}</h1>"

if __name__ == '__main__':
    app.run(debug=True)