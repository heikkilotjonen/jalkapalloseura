import sqlite3
from flask import Flask
from flask import redirect, render_template, request
from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.route("/")
def index():
    return "Tähän tulee jalkapalloseura sovellus"

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        db = sqlite3.connect("database.db")
        db.isolation_level = None
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        db.close()
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"