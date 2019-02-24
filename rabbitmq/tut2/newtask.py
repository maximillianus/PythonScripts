'''
This python code will send single message to rabbitmq's queue
'''

#1/usr/bin/env python3
import pika
import sys
from datetime import datetime

# establish connection with rabbitmq-server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create 'task_queue' which has durable property
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or 'Hello World! the time now is %s' % datetime.now()
# tells channel which exchange to publish to
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2   # makes message persistent
                      ))
print(" [x] sent %r" % message)

# close conn
connection.close()
