"""viewings module"""
from db import db
import users

def add_user_info_viewing(user_id: int):
    """User info viewings data updated"""
    current_user_id = users.get_current_user_id()
    if current_user_id is False:
        current_user_id = None
    sql = "INSERT INTO userviewings (user_id, viewer, viewed) VALUES (:user_id, :viewer, NOW())"
    db.session.execute(sql, {"user_id":user_id, "viewer":current_user_id})
    db.session.commit()

def get_user_info_viewings(user_id: int, only_registered_users=True):
    """How many logged in users have seen user info"""

    if only_registered_users is True:

        # sql = "SELECT id, user_id, viewer, viewed FROM userviewings WHERE user_id=:user_id GROUP BY viewer"
        sql = "SELECT viewer FROM userviewings WHERE user_id=:user_id GROUP BY viewer"
        result_obj = db.session.execute(sql, {"user_id":user_id})
        viewings_list = result_obj.fetchall()

    else:
        sql = "SELECT id, user_id, viewer, viewed FROM userviewings WHERE user_id=:user_id"
        result_obj = db.session.execute(sql, {"user_id":user_id})
        viewings_list = result_obj.fetchall()
    return viewings_list

def get_user_info_newest_viewing(user_id: int, only_registered_users=True):
    """Get newest user info viewing (other than user itself)"""

    if only_registered_users is True:
        sql = "SELECT id, user_id, viewer, viewed FROM userviewings WHERE user_id=:user_id AND viewer!=user_id GROUP BY viewer "
        result_obj = db.session.execute(sql, {"user_id":user_id})
        viewings_list = result_obj.fetchall()
    else:
        sql = "SELECT id, user_id, viewer, viewed FROM userviewings WHERE user_id=:user_id AND viewer!=user_id"
        result_obj = db.session.execute(sql, {"user_id":user_id})
        viewings_list = result_obj.fetchall()
    return viewings_list[0]