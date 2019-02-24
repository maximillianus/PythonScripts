'''
This python code will receive single message to rabbitmq's queue
'''

#1/usr/bin/env python3
import pika

# establish connection with rabbitmq-server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create 'hello' queue to which message will be delivered
# good to re-declare queue to ensure queue exists
# queue declaration is idempotent and only one will be created
channel.queue_declare(queue='hello')

# callback function to print content
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# next we need to tell rabbitmq that this callback function should
# receive message from 'hello' queue
channel.basic_consume(consumer_callback=callback, 
                      queue='hello', 
                      no_ack=True)

# Go into loop to watch messages
print(" [*] Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()
