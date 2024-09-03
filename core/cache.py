import redis
import json
from time import time
from dotenv import load_dotenv
load_dotenv()
from os import getenv

# from  core.redis_pub import pub

# local redis server
# redis_client = redis.Redis(host='localhost',port=6379,db=5)

# connection to neon redis server
redis_replica = redis.Redis(
  host=getenv('REDIS_HOST_CLOUD'),
  port=getenv('REDIS_PORT_CLOUD'),
  password=getenv('REDIS_PASS_CLOUD'))

# connection to redis oranage zebra 
redis_main = redis.Redis(
  host=getenv('REDIS_HOST_VERCEl'),
  port=getenv('REDIS_PORT_VERCEL'),
  password=getenv('REDIS_PASS_VERCEL'))


# add value to 
def insert(key,val,ex=None):
    # pub("redis_cache","Todo {key} cached")
    val = json.dumps(val).encode('utf-8')
    if ex:
        redis_main.set(key,val,ex)
        redis_replica.set(key,val,ex)
        return 
    redis_main.set(key,val)

def fetch(key):
    # pub("redis_cache","Todo {key} fetched")
    if redis_main.exists(key):
        data=redis_main.get(key).decode('utf-8')
        return json.loads(data)
    return None

def delete(key):
    # pub("redis_cache","Todo  {key} deleted")
    if redis_main.exists(key):
        redis_main.delete(key)
        redis_replica.delete(key)
        return True
    return False

def exists(key):
    return bool (redis_main.exists(key))
