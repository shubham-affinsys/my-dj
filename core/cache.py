import redis
import json
from time import time
from dotenv import load_dotenv
load_dotenv()
from os import getenv

# from  core.redis_pub import pub

# local redis server
# redis_client = redis.Redis(host='localhost',port=6379,db=5)

redis_client = redis.Redis(
  host='redis-11304.c275.us-east-1-4.ec2.redns.redis-cloud.com',
  port=11304,
  password=getenv('REDIS_PASS'))


# add value to 
def insert(key,val,ex=None):
    # pub("redis_cache","Todo {key} cached")
    val = json.dumps(val).encode('utf-8')
    if ex:
        redis_client.set(key,val,ex)
        return 
    redis_client.set(key,val)

def fetch(key):
    # pub("redis_cache","Todo {key} fetched")
    if redis_client.exists(key):
        data=redis_client.get(key).decode('utf-8')
        return json.loads(data)
    return None

def delete(key):
    # pub("redis_cache","Todo  {key} deleted")
    if redis_client.exists(key):
        redis_client.delete(key)
        return True
    return False

def exists(key):
    return bool (redis_client.exists(key))
