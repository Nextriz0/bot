import time

cooldowns = {}

def check(user_id, key, delay):
    now = time.time()

    if user_id not in cooldowns:
        cooldowns[user_id] = {}

    last = cooldowns[user_id].get(key, 0)

    if now - last < delay:
        return False

    cooldowns[user_id][key] = now
    return True
