"""routers module"""
from app import app
from flask import redirect, render_template, request, session
import users, trainings

@app.route("/")
def index():
    # Get all users
    # result_obj = db.session.execute("SELECT username FROM users")
    # users = result_obj.fetchall()
    new_users_list = users.get_new_users_list()
    return render_template("index.html", user_count=len(new_users_list), users=new_users_list)

@app.route("/view_users")
def view_users():
    # Get all users
    # result_obj = db.session.execute("SELECT username FROM users")
    # users = result_obj.fetchall()
    all_users_list = users.get_users_list()
    return render_template("view_users.html", user_count=len(all_users_list), users=all_users_list)

@app.route("/login",methods=["GET", "POST"])
def login():
    """Render login user page"""
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if password is correct
        resp = users.login(username, password)
        if resp == True:
            return redirect("/")
        else:
            # TODO some error message index page
            return redirect("/")

@app.route("/register",methods=["GET", "POST"])
def register():
    """Render register new user page and redirect main page"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    resp = users.register(username, password)

    # Log in if registering was succesfull
    if resp == True:
        resp_login = users.login(username, password)
        if resp_login == True:
            return redirect("/")
        else:
            print("Failed to login")
            return redirect("/")
    else:
        print("Failed to register")
        return redirect("/")

@app.route("/logout")
def logout():
    """Render logout and redirect main page"""
    users.logout()
    return redirect("/")

@app.route("/entry")
def entry():
    """Entry new training page render"""
    return render_template("entry.html")

@app.route("/save_entry", methods=["POST"])
def save_entry():
    """Save new training entry and redirect trainings list page"""
    content = request.form["content"]
    if len(content) > 10000:
        return render_template("error.html", error_message="Training entry longer than limit 10000 characters")
    else:
        date = request.form["date"]
        print(date)
        resp = trainings.save_entry(content, date)
        if resp == True:
            return redirect("/trainings")
        else:
            return render_template("entry.html")

@app.route("/trainings")
def show_trainings():
    """Render trainings page showing all user trainings"""

    # trainings = ["training_string_dummy1", "training_string_dummy2", "training_string_dummy3"]
    # training_count="3"

    # user_id = session["user_id"]
    # sql = "SELECT content FROM trainings WHERE user_id=:user_id"
    # result_obj = db.session.execute(sql, {"user_id":user_id})
    # trainings = result_obj.fetchall()

    user_id = session["user_id"]
    trainings_list = trainings.get_list(user_id)

    if trainings_list == False:
        trainings_list = ["Not allowed to show trainings"]
    else:
        return render_template("trainings.html", training_count=len(trainings_list), trainings=trainings_list)