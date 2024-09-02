import redis
from datetime import datetime
redis_client = redis.Redis(host='localhost',port=6379,db=7)

def pub(channel,action):
    redis_client.publish(channel,f"[{datetime.now()}] --- channel: {channel} --- action --> {action}")

def my_debugger(action):
    pub(channel="my_debugger_queue",action=action)