import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

from helper import apology, login_required, lookup, usd

# Flask app initialisation
app = Flask(__name__)
app.secret_key = os.urandom(24)  # or use a custom secret key

def get_db_connection():
    con = sqlite3.connect('trippa.db', check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

db = get_db_connection()

@app.route("/", methods=["GET"])
@login_required
def index():
    user_id = session["user_id"]
    return render_template("index.html", username=user_id)


# User Management (Register, Log in, Log Out)
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password:
            error = "Must provide a username and password"
            return render_template("error.html", error=error) 

        if password != confirmation:
            error = "Passwords must match"
            return render_template("error.html", error=error)

        # Query database for username
        existing_user = db.execute("SELECT username FROM users WHERE username = ?", (username,))[0]["username"]
        if existing_user:
            db.close()
            error = "User already exists"
            return render_template("error.html", error=error)

        # Insert the new user into the database
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
        db.commit()
        db.close()

        flash("Registered successfully!")
        return redirect(url_for("login"))

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

        user = ("SELECT username FROM users WHERE username = ?", (username))[0]["username"]            
        if not user or not check_password_hash(user.hash, password):
            db.close()
            return "Invalid username and/or password"

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