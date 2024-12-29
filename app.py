import os

from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from flask_session import session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

# Flask app initialisation
app = Flask(__name__)

# Database configuration
DATABASE = 'trippa.db'

# Function to get the database connection
def get_db():
    if 'db' not in g: # Check if 'db' is already stored in the application context
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row # Return rows as dictionaries for easier access
    return g.db

    # Close the database connection when the request ends
    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

# Create a cursor to execute SQL commands
cursor = con.cursor()