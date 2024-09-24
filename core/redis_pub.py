import redis
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from os import getenv

redis_client = redis.Redis(
  host=getenv('REDIS_HOST_VERCEl'),
  port=getenv('REDIS_PORT_VERCEL'),
  password=getenv('REDIS_PASS_VERCEL'))


def pub(channel,action):
    redis_client.publish(channel,f"[{datetime.now()}] --- channel: {channel} --- action --> {action}")

def my_debugger(action):
    pub(channel="my_debugger_queue",action=action)