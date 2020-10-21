from flask import Flask, redirect, url_for, render_template, request, session, flash
app = Flask(__name__)

app.secret_key = "Super secret key!!!"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        session["user"] = user;
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route('/logout')
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
        session.pop("user", None)
    return redirect(url_for("home"))   

@app.route('/user')
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)