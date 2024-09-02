import redis

"""
connected to redis db 5
functions:
     insert
     fetch
"""
redis_client = redis.Redis(host="localhost", db=5)


def insert(key, val, exp=None):
    if redis_client.exists(key):
        pass
    if exp:
        redis_client.set(key, val, ex=exp)
    else:
        redis_client.set(key, val)


def fetch(key):
    val = redis_client.get(key)
    return val


def exists(key):
    if redis_client.exists(key):
        return True
    return False


def get_all():
    key_list = redis_client.keys("*")
    data = dict()
    for key in key_list:
        key = key.decode('utf-8')
        data[key]= redis_client.get(key).decode('utf-8')
    return data


# insert("shubh","Hello I am Shubh")
# print(get_all())