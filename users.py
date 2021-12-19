"""Users module"""
from datetime import datetime
# from os import error
import secrets
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    """Copied from course materials
    https://hy-tsoha.github.io/materiaali/osa-3/#sovelluksen-rakenne
    """
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False

    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return True

    return False


def register(username, password):
    """According course material
    https://hy-tsoha.github.io/materiaali/osa-3/#sovelluksen-rakenne
    """
    hash_value = generate_password_hash(password)
    current_time_str = str(datetime.now())
    print(f"current_time_str = {current_time_str}")
    try:
        sql = "INSERT INTO users (username, password, registered1, \
            registered2, registered3, public) VALUES (:username, :password, \
            :registered1, :registered2, NOW(), :public)"
        db.session.execute(sql, {"username":username, "password":hash_value,
            "registered1":current_time_str, "registered2":current_time_str, "public":True})
        db.session.commit()
    except Exception as expection_:
        print(f"Failed to register user because: {expection_}")
        return False
    return True


def get_new_users_list():
    """Get 5 newest users list from database"""
    sql = "SELECT id, username, registered3 FROM users WHERE public=:public \
        ORDER BY registered3 LIMIT 5"
    result_obj = db.session.execute(sql, {"public":True})
    new_users_list = result_obj.fetchall()
    return new_users_list


def get_users_list():
    """Get users list from database where public is True"""
    sql = "SELECT username, registered3, id FROM users WHERE public=:public"
    result_obj = db.session.execute(sql, {"public":True})
    all_users_list = result_obj.fetchall()
    return all_users_list


def logout():
    """Logout user"""
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]


def get_current_user_id():
    """Get current user id from session"""
    user_id = session.get("user_id", False)
    return user_id


def get_user_info(user_id):
    """Get user info based on user id"""

    current_user_id = get_current_user_id()

    if user_id == current_user_id:
        sql = "SELECT id, username, registered3, id FROM users WHERE id=:user_id"
        result_obj = db.session.execute(sql, {"user_id":user_id})
        user_info = result_obj.fetchall()

    elif user_id != current_user_id:
        sql = "SELECT id, username, registered3, id FROM users WHERE id=:user_id AND public=:public"
        result_obj = db.session.execute(sql, {"user_id":user_id, "public":True})
        user_info = result_obj.fetchall()

    if len(user_info) == 1 and "id" in user_info[0].keys():
        return user_info[0]
    return False
