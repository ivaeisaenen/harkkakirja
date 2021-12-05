"""trainings module"""
from db import db
import users

def save_entry(content, workout_day):
    # # TODO check user exist and is logged in?
    # sql = "SELECT id FROM users WHERE username=:username"
    # db.session.execute(sql, {"username":username})
    # result = db.session.execute(sql, {"username":username})
    # user = result.fetchone()
    # user_id = user.id

    user_id = users.get_user_id()
    if user_id == False:
        print("Could not get user_id")
        return False
    else:
        print("save_entry_trainings")
        sql = "INSERT INTO trainings (content, workout_day, user_id, sent_at) VALUES (:content, :workout_day, :user_id, NOW())"
        db.session.execute(sql, {"content":content, "workout_day":workout_day, "user_id":user_id})
        db.session.commit()
        return True

def get_list(user_id):
    # check if user is trying to look own trainings
    current_user_id = users.get_user_id()
    if user_id == current_user_id:
        sql = "SELECT content FROM trainings WHERE user_id=:user_id"
        result_obj = db.session.execute(sql, {"user_id":user_id})
        trainings_list = result_obj.fetchall()
        return trainings_list
    # if not own trainings check if targeted user exist and if his trainings are public
    # TODO check if trainings are public, for now, all trainings are private
    else:
        return False