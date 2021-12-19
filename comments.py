"""comments module"""
from db import db
import users
import trainings

def save_training_comment(user_id, training_id, content):
    """Save training comment to database"""

    user_id_ = users.get_current_user_id()
    if user_id is False:
        return False
    elif user_id != user_id_:
        return False

    userinfo = users.get_user_info(user_id)
    if userinfo is False:
        return False
    username = userinfo["username"]

    # Check if training id is there
    if trainings.check_if_training_exists(training_id) is False:
        return False

    sql = "INSERT INTO trainingcomments (content, receiver, sender, sender_name, sent_at) \
            VALUES (:content, :receiver, :sender, :sender_name, NOW())"
    db.session.execute(sql, {"content":content,
                             "receiver":training_id,
                             "sender":user_id,
                             "sender_name":username})
    db.session.commit()
    return True


def get_training_comments(training_id: int):
    """Get list of training comment based on training_id value from database TABLE trainingcomments"""

    current_user_id = users.get_current_user_id()
    if current_user_id is False:
        return ["User not logged in"]
    sql = "SELECT id, content, receiver, sender, sender_name, sent_at FROM trainingcomments WHERE receiver=:training_id ORDER BY sent_at"
    result_obj = db.session.execute(sql, {"training_id":training_id})
    training_comments_list = result_obj.fetchall()
    return training_comments_list
