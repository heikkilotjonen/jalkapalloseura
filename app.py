import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import config, forum, users

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
    if len(title) > 100 or len(content) > 5000:
        abort(403)
    return redirect("/notice/" + str(notice_id))

@app.route("/notice/<int:notice_id>")
def show_notice(notice_id):
    notice = forum.get_notice(notice_id)
    if not notice:
        abort(404)
    signings = forum.get_signings(notice_id)
    return render_template("notice.html", notice=notice, signings=signings)

@app.route("/edit/<int:notice_id>", methods=["GET", "POST"])
def edit_notice(notice_id):
    notice = forum.get_notice(notice_id)
    if notice["use_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", notice=notice)

    if request.method == "POST":
        content = request.form["content"]
        forum.update_notice(notice["id"], content)
        return redirect("/notice/" + str(notice_id))

@app.route("/remove/<int:notice_id>", methods=["GET", "POST"])
def del_notice(notice_id):
    notice = forum.get_notice(notice_id)

    if request.method == "GET":
        return render_template("remove.html", notice=notice)

    if request.method == "POST":
        if "continue" in request.form:
            forum.remove_notice(notice_id)
            return redirect("/")
        else:
            return redirect("/notice/" + str(notice_id))
        
@app.route("/search")
def search():
    query = request.args.get("query")
    results = forum.search(query) if query else []
    return render_template("search.html", query=query, results=results)
    
@app.route("/sign_up/<int:notice_id>", methods=["POST"])
def sign_up(notice_id):
    user_id = session["user_id"]
    if not forum.is_user_signed_up(user_id, notice_id):
        signing_id = forum.add_signing(user_id, notice_id)
    return redirect("/notice/" + str(notice_id))

@app.route("/del_sign_up/<int:notice_id>", methods=["GET", "POST"])
def del_sign_up(notice_id):
    user_id = session["user_id"]
    signing_id = forum.get_signing(notice_id, user_id)
    forum.del_signing(signing_id)
    return redirect("/notice/" + str(notice_id))

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
    if "user_id" in session:
        del session["user_id"]
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
        return render_template("passworderror.html")
    password_hash = generate_password_hash(password1)

    try:
        db = sqlite3.connect("database.db")
        db.isolation_level = None
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        db.close()
    except sqlite3.IntegrityError:
        return render_template("existingaccount.html")
    
    return render_template("created.html")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    
    own_notices = users.get_own_notices(user_id)
    signed_notices = users.get_signed_notices(user_id)
    
    return render_template("user.html", user=user, own_notices=own_notices, signed_notices=signed_notices)