"""users module"""
from datetime import datetime
from os import error
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
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


def register(username, password):
    """According course material
    https://hy-tsoha.github.io/materiaali/osa-3/#sovelluksen-rakenne
    """
    hash_value = generate_password_hash(password)
    current_time_str = str(datetime.now())
    print(f"current_time_str = {current_time_str}")
    try:
        sql = "INSERT INTO users (username, password, registered1, registered2, registered3) VALUES (:username, :password, :registered1, :registered2, NOW())"
        db.session.execute(sql, {"username":username, "password":hash_value, "registered1":current_time_str, "registered2":current_time_str})
        db.session.commit()
    except Exception as e:
        print(f"Failed to register user because: {e}")
        return False
    return True

def get_new_users_list():
    """Get 5 newest users list from database"""
    result_obj = db.session.execute("SELECT username, registered3 FROM users ORDER BY registered1 LIMIT 5")
    new_users_list = result_obj.fetchall()
    return new_users_list

def get_users_list():
    """Get users list from database"""
    result_obj = db.session.execute("SELECT username, registered3 FROM users")
    all_users_list = result_obj.fetchall()
    return all_users_list

def logout():
    """Logout user"""
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]

def get_user_id():
    user_id = session.get("user_id", False)
    return user_id