from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///harkkakirja"
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
    # Get all users
    result_obj = db.session.execute("SELECT username FROM users")
    users = result_obj.fetchall()
    return render_template("index.html", user_count=len(users), users=users)

def login_user(username, password):
    """Copied from course materials
    https://hy-tsoha.github.io/materiaali/osa-3/#sovelluksen-rakenne
    """
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            return True
        else:
            return False

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Check if password is correct
        resp = login_user(username, password)
        if resp == True:
            return redirect("/")
        else:
            # TODO some error message index page
            return redirect("/")

def register_user(username, password):
    """According course material
    https://hy-tsoha.github.io/materiaali/osa-3/#sovelluksen-rakenne
    """
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return True

@app.route("/register",methods=["GET", "POST"])
def register():
    """According course material
    https://hy-tsoha.github.io/materiaali/osa-3/#sovelluksen-rakenne
    """
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    resp = register_user(username, password)
    if resp == True:
        resp_login = login_user(username, password)
        if resp_login == True:
            return redirect("/")
    return redirect("/")


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]
    return redirect("/")

@app.route("/entry")
def entry():
    return render_template("entry.html")

def save_entry_trainings(content, date):
    user_id = session["user_id"]

    # # TODO check user exist and is logged in?
    # sql = "SELECT id FROM users WHERE username=:username"
    # db.session.execute(sql, {"username":username})
    # result = db.session.execute(sql, {"username":username})
    # user = result.fetchone()
    # user_id = user.id
    print("save_entry_trainings")
    sql = "INSERT INTO trainings (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True    


@app.route("/save_entry", methods=["POST"])
def save_entry():
    content = request.form["content"]
    date = request.form["date"]
    print(date)
    resp = save_entry_trainings(content, date)
    if resp == True:
        return redirect("/trainings")
    else:
        return render_template("entry.html")

@app.route("/trainings")
def trainings():
    # trainings = ["training_string_dummy1", "training_string_dummy2", "training_string_dummy3"]
    # training_count="3"
    user_id = session["user_id"]
    sql = "SELECT content FROM trainings WHERE user_id=:user_id"
    result_obj = db.session.execute(sql, {"user_id":user_id})
    trainings = result_obj.fetchall()
    return render_template("trainings.html", training_count=len(trainings), trainings=trainings)

# print(dir(db))