'''
This python code will send single message to rabbitmq's queue
'''

#1/usr/bin/env python3
import pika
from datetime import datetime

# establish connection with rabbitmq-server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create 'hello' queue to which message will be delivered
channel.queue_declare(queue='hello')

msg = 'Hello World! the time now is %s' % datetime.now()
# tells channel which exchange to publish to
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=msg)
print(" [x] Sent 'Hello World!'")

# close conn
connection.close()
