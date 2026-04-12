import random
from db.sqlite import get_user, update

def dig(user_id):
    user = get_user(user_id)

    money = random.randint(10, 80)
    bones = random.randint(1, 4)
    bottle = 1 if random.random() < 0.2 else 0

    update(user_id, "money", user[1] + money)
    update(user_id, "bones", user[2] + bones)
    update(user_id, "bottles", user[3] + bottle)

    return money, bones, bottle
