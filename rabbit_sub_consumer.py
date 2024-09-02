import pika
import json
from core.redis_pub import my_debugger
import time
def email_sender(email,message):
    print("sending email")
    print("email sent")
    print(email,message)



def callback(ch,method,properties,body):
    # print("ch: ",ch)
    # print("method: ",method)
    # print("proprties: ",properties)
    # print(body.decode())
    try:
        data = json.loads(body)
        email = data.get("email")
        message = data.get("message")

        email_sender(email=email,message=message)
        my_debugger(action=f"queue: {queue}mail sent ===> body:{body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        # handle message rejection or reque the message
        my_debugger(action=f"error occured while processing the message ====> {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag,requeue=True)

try:
    params = pika.URLParameters("amqps://sjqnwwmv:32FMj2zVoG-3U37PuWFth7nWJIu7cRuw@puffin.rmq2.cloudamqp.com/sjqnwwmv")
    queue="mq_queue"
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=queue,durable=True)
    channel.basic_consume(queue=queue,on_message_callback=callback,auto_ack=False)

    print(f"Ready to consume on {queue}")

    channel.start_consuming()
except Exception as e:
    my_debugger(action=f"error occured when trying to consume the message{e}")
