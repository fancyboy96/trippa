import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from helper import apology, login_required, lookup, usd

# Flask app initialisation
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trippa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey' # REPLACE!!

#Initialise database
db = SQLAlchemy(app)


@app.route("/")
def index():
    return("Hello World!")


# User Management (Register, Log in, Log Out)
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        flash("Registered successfully!")
        return(redirect(url_for("login")))
    else:
        return render_template("register.html")
    return("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login user"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Must provide username and password"

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.hash, password):
            return "Invalid username or password"

        session["user_id"] = user.id
        flash("Logged in successfully!")
        return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)