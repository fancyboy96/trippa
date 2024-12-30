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

class User(db.Model):  # db.Model is a declarative base class
    __tablename__ = 'users'  # This explicitly maps the model to the 'users' table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)


@app.route("/")
def index():
    return("Hello World!")


# User Management (Register, Log in, Log Out)
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            error = "Must provide a username and password"
            return render_template("error.html", error=error) 

        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            error = "User already exists"
            return render_template("error.html", error=error)
        
        flash("Registered successfully!")
        return(redirect(url_for("login")))

        # Hash password and add user to the database
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    else:
        return render_template("register.html")


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