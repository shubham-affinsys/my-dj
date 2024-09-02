import pika
import json
from vege.models import User
import atexit
from core.redis_pub import my_debugger
import logging
logger = logging.getLogger("mydj")

# make connection to rabbitmq
# create a channel in connection
# declare a queue in channel

"""
connect a remote rabbitmq server:
params = pika.URLParameters("amqps://sjqnwwmv:32FMj2zVoG-3U37PuWFth7nWJIu7cRuw@puffin.rmq2.cloudamqp.com/sjqnwwmv")
connection = pika.BlockingConnection(params)

connect local host rabbitMQ server:
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

"""

try:
    params = pika.URLParameters("amqps://sjqnwwmv:32FMj2zVoG-3U37PuWFth7nWJIu7cRuw@puffin.rmq2.cloudamqp.com/sjqnwwmv")
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare("mq_queue",durable=True) # durable will make queue persist even if rabbit mq restarts
except Exception as e:
    my_debugger(f"error connecting to rabbitMQ: {e}")
    connection=None


def publish_message(user,message):
    if not connection:
        my_debugger("error =======>  Connection to RabbitMQ not established")
        return
    
    try:
        user_email = User.objects.get(username=user).email
        data ={
                "email":user_email,
                "message":message
                }
        # channel = connection.channel()
        channel.basic_publish(exchange="",
                            routing_key="mq_queue",
                            body=json.dumps(data),
                            properties=pika.BasicProperties(
                                delivery_mode=2
                            )
                        )    
    except Exception as e:
        my_debugger(f"error publishing message: {e}")
    # finally :
    #     if connection:
    #         channel.close()
    #         connection.close()

def close_rabbitmq_connection():
    if connection and connection.is_open:
        channel.close()
        connection.close()
        my_debugger("RabbitMQ connection and channel closed.")

# Register the cleanup function to be called on program exit
try:
    atexit.register(close_rabbitmq_connection)
except Exception as e:
    logger.error(f"error occured while clossing rabbitMQ connection: {e}")