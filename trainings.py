"""trainings module"""
from db import db
import users

def save_entry(topic, content, workout_day):
    """Save training log entry to database"""

    user_id = users.get_current_user_id()
    if user_id is False:
        return False

    sql = "INSERT INTO trainings (topic, content, workout_day, user_id, public, sent_at) \
            VALUES (:topic, :content, :workout_day, :user_id, :public, NOW())"
    db.session.execute(sql, {"topic":topic,
                                "content":content,
                                "workout_day":workout_day,
                                "user_id":user_id,
                                "public":True})
    db.session.commit()
    return True


def get_list(user_id):
    """Get list of trainings based on user_id value from database TABLE trainings"""

    current_user_id = users.get_current_user_id()

    if user_id == current_user_id:
        sql = "SELECT id, user_id, topic, content, workout_day, sent_at FROM trainings \
                WHERE user_id=:user_id"
        result_obj = db.session.execute(sql, {"user_id":user_id})
        trainings_list = result_obj.fetchall()
        return trainings_list

    if user_id != current_user_id:
        sql = "SELECT id, user_id, topic, content, workout_day, sent_at FROM trainings \
                WHERE user_id=:user_id AND public=:public"
        result_obj = db.session.execute(sql, {"user_id":user_id, "public":True})
        trainings_list = result_obj.fetchall()
        return trainings_list
    return False

def get_new_trainings():
    """Get list of 3 newest trainings based on user_id value from database TABLE trainings"""

    current_user_id = users.get_current_user_id()

    if current_user_id is False:
        sql = "SELECT t.id, t.user_id, u.username, t.topic, t.content, t.workout_day, t.sent_at \
                FROM trainings t LEFT JOIN users u ON t.user_id = u.id WHERE t.public=:public \
                ORDER BY t.sent_at LIMIT 3"
        result_obj = db.session.execute(sql, {"public":True})
        trainings_list = result_obj.fetchall()
    else:
        sql = "SELECT t.id, t.user_id, u.username, t.topic, t.content, t.workout_day, t.sent_at \
                FROM trainings t LEFT JOIN users u ON t.user_id = u.id WHERE t.user_id=:user_id \
                OR t.public=:public ORDER BY t.sent_at LIMIT 3"
        result_obj = db.session.execute(sql, {"user_id":current_user_id, "public":True})
        trainings_list = result_obj.fetchall()

    return trainings_list


def get_training(training_id: int):
    """Get training data based on training_id from database TABLE trainings"""
    # check if user is trying to look own trainings
    # current_user_id = users.get_current_user_id()

    current_user_id = users.get_current_user_id()

    sql = "SELECT t.id, t.user_id, u.username, t.topic, t.content, t.workout_day, t.sent_at \
            FROM trainings t LEFT JOIN users u ON u.id = t.user_id WHERE t.id=:training_id \
            AND (t.public=:public OR t.user_id=:user_id)"
    result_obj = db.session.execute(sql, {"training_id":training_id, "public":True, \
                                        "user_id":current_user_id})
    trainings_list = result_obj.fetchall()
    if len(trainings_list) == 1:
        return trainings_list[0]
    return False


def check_if_training_exists(training_id: int):
    """Check if training_id is found in the database TABLE trainings as primary key"""
    sql = "SELECT trainings.id FROM trainings WHERE id=:training_id"
    result_obj = db.session.execute(sql, {"training_id":training_id})
    trainings_list = result_obj.fetchall()
    if len(trainings_list) == 1:
        return True
    return False
