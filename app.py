import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, flash
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import config, forum, users, math, secrets, markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    notice_count = forum.notice_count()
    page_count = math.ceil(notice_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))
    
    notices = forum.get_notices(page, page_size)
    return render_template("frontpage.html", page=page, page_count = page_count, notices=notices)

@app.route("/new_notice", methods=["POST"])
def new_notice():
    check_csrf()
    title = request.form["title"]
    content = request.form["content"]
    level = request.form["level"]
    location = request.form["location"]
    date = request.form["date"]
    user_id = session["user_id"]

    notice_id = forum.add_notice(title, content, level, location, date, user_id)
    if len(title) > 100 or len(content) > 5000:
        abort(403)
    return redirect("/notice/" + str(notice_id))

@app.route("/notice/<int:notice_id>")
def show_notice(notice_id):
    notice = forum.get_notice(notice_id)
    signings = forum.get_signings(notice_id)
    return render_template("notice.html", notice=notice, signings=signings)

@app.route("/edit/<int:notice_id>", methods=["GET", "POST"])
def edit_notice(notice_id):
    notice = forum.get_notice(notice_id)
    if notice["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", notice=notice)

    if request.method == "POST":
        content = request.form["content"]
        level = request.form["level"]
        location = request.form["location"]
        date = request.form["date"]
        forum.update_notice(notice["id"], content, level, location, date)
        return redirect("/notice/" + str(notice_id))

@app.route("/remove/<int:notice_id>", methods=["GET", "POST"])
def del_notice(notice_id):
    notice = forum.get_notice(notice_id)
    if notice["user_id"] != session["user_id"]:
        abort(403)

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

    result = users.login(username)

    if result:
        user_id, password_hash = result
        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: Väärä tunnus tai salasana")
            return redirect("/login")
    else:
        flash("VIRHE: Väärä tunnus tai salasana")
        return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})
    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 16:
            abort(403)

        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("VIRHE: Salasanat eivät täsmää")
            filled = {"username": username}
            return render_template("register.html", filled=filled)
        
        password_hash = generate_password_hash(password1)

        try:
            users.create_account(username, password_hash)
        except sqlite3.IntegrityError:
            flash("VIRHE: Tunnus on jo varattu")
            filled = {"username": username}
            return render_template("register.html", filled=filled)
        
        result = users.login(username)  

        if result:
            user_id, stored_password_hash = result
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")  
        else:
            flash("VIRHE: Rekisteröinti onnistui, mutta kirjautuminen epäonnistui.")
            return redirect("/login")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)

    page_size = 20

    notice_count = users.own_notices_count(user_id)
    signing_count = users.signed_notices_count(user_id)
    
    notice_page_count = math.ceil(notice_count / page_size)
    signed_page_count = math.ceil(signing_count / page_size)

    notice_page = request.args.get('notice_page', 1, type=int)
    signed_page = request.args.get('signed_page', 1, type=int)

    own_notices = users.get_own_notices(user_id, (notice_page - 1) * page_size, page_size)
    signed_notices = users.get_signed_notices(user_id, (signed_page - 1) * page_size, page_size)

    return render_template("user.html", user=user, own_notices=own_notices, signed_notices=signed_notices, notice_page=notice_page, signed_page=signed_page, 
                           notice_page_count=notice_page_count, signed_page_count=signed_page_count)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)