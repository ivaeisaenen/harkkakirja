"""Routes module"""
from flask import redirect, render_template, request, session
from app import app
import users
import trainings
import comments
import viewings

@app.route("/")
def index():
    """Render the main aka index page"""
    new_users_list = users.get_new_users_list()
    new_trainings_list = trainings.get_new_trainings()

    return render_template("index.html", user_count=len(new_users_list), users=new_users_list, new_trainings_list=new_trainings_list)


@app.route("/view_users")
def view_users():
    """Render view all users page"""
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
        if resp is True:
            return redirect("/")

        error_message = "Failed to login"
        return render_template("error.html", error_message=error_message)
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
    if resp is True:
        resp_login = users.login(username, password)
        if resp_login is True:
            return redirect("/")
        error_message = "Failed to login"
        return render_template("error.html", error_message=error_message)

    error_message = "Failed to register"
    return render_template("error.html", error_message=error_message)


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
    topic = request.form["topic"]
    content = request.form["content"]
    date = request.form["date"]

    if len(topic) > 160:
        return render_template("error.html",
                error_message="Training entry topic longer than limit 160 characters")

    if len(content) > 10000:
        return render_template("error.html",
                error_message="Training entry longer than limit 10000 characters")


    resp = trainings.save_entry(topic, content, date)
    if resp is True:
        return redirect("/trainings")

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

    if trainings_list is False:
        trainings_list = ["Not allowed to show trainings"]

    return render_template("trainings.html",
            training_count=len(trainings_list), trainings=trainings_list)


@app.route("/user_info/<int:id>")
def user_info(id):
    """Render user info page"""

    # Add view to viewings
    viewings.add_user_info_viewing(id)

    user_info = users.get_user_info(id)
    if user_info is False:
        return render_template("error.html",
                error_message="Failed to get user info")

    trainings_list = trainings.get_list(id)
    if trainings_list is False:
        return render_template("error.html",
                error_message="Failed to get trainings list")


    registered_viewings = viewings.get_user_info_viewings(id, only_registered_users=True)
    number_of_registered_views = len(registered_viewings)

    return render_template("user_info.html", user_info=user_info, training_count=len(trainings_list), trainings=trainings_list, number_of_registered_views=number_of_registered_views)


@app.route("/training/<int:id>")
def show_training(id):
    """Render individual training page"""

    if id is None:
        return render_template("error.html", error_message="Invalid training id")

    # user_info = users.get_user_info(id)
    training = trainings.get_training(id)
    if training is False:
        return render_template("error.html", error_message="Failed to find training")

    comments = trainings.get_training_comments(id)
    viewings = trainings.get_training_viewings(id)
    number_of_views = len(viewings)
    userinfo = users.get_user_info(training["user_id"])
    trainername = userinfo["username"]

    return render_template("training.html", training=training, comments=comments, number_of_views=number_of_views, trainername=trainername)


@app.route("/leave_comment",methods=["GET", "POST"])
def leave_comment():
    """leave training comment"""

    if request.method == "POST":
        training_id_ = request.form["training_id"]
        training_id = int(training_id_)
        user_id = session["user_id"]
        if user_id is False:
            return render_template("error.html",
                    error_message="Failed to get user id! Please login.")
        content = request.form["content"]
        if len(content) > 10000:
            return render_template("error.html",
                    error_message="Comment entry longer than limit 10000 characters")
        resp = comments.save_training_comment(user_id, training_id, content)
        if resp is False:
             return render_template("error.html", error_message="Failed to leave a comment")
    return redirect(f"/training/{training_id}")
