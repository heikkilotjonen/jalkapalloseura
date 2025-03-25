import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import config, forum

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    notices = forum.get_notices()
    return render_template("frontpage.html", notices=notices)

@app.route("/new_notice", methods=["POST"])
def new_notice():
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]

    notice_id = forum.add_notice(title, content, user_id)
    return redirect("/notice/" + str(notice_id))

@app.route("/notice/<int:notice_id>")
def show_notice(notice_id):
    connection = get_db_connection()
    notice = connection.execute('SELECT * FROM notices WHERE id = ?', (notice_id,)).fetchone()
    connection.close()
    return render_template("notice.html", notice=notice)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    with sqlite3.connect("database.db") as db:
        db.isolation_level = None
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        cursor = db.execute(sql, [username])
        result = cursor.fetchone()

    if result:
        user_id, password_hash = result
        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

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