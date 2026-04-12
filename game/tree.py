import random
import time
from db.sqlite import get_user, update

def water_tree(user_id):
    user = get_user(user_id)
    now = int(time.time())

    if now - user[6] < 14400:
        return None

    grow = round(random.uniform(0.1, 1.5), 2)

    update(user_id, "tree", user[5] + grow)
    update(user_id, "last_water", now)

    return grow


def fertilize(user_id):
    user = get_user(user_id)

    if user[4] < 1:
        return False

    update(user_id, "dust", user[4] - 1)
    return True
