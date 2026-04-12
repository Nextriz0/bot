from db.sqlite import get_user, update

def add_chat_point(user_id):
    user = get_user(user_id)
    update(user_id, "daily_rating", user[7] + 1)
