'''
This python code will receive single message to rabbitmq's queue
'''

#1/usr/bin/env python3
import pika
import time

# establish connection with rabbitmq-server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create 'task_queue' which has durable property
channel.queue_declare(queue='task_queue', durable=True)

# callback function to print content
def callback(ch, method, properties, body):
    print(" [x] received %r" % body)
    time.sleep(body.count(b'.'))
    print(' [x] Done')
    ch.basic_ack(delivery_tag = method.delivery_tag) # ensure received msg is acknowledged

# add prefetch count property for worker to consume only
# if they are not busy
channel.basic_qos(prefetch_count=1)

# next we need to tell rabbitmq that this callback function should
# receive message from 'hello' queue
channel.basic_consume(consumer_callback=callback, 
                      queue='hello', 
                      no_ack=False) # ensure received msg is acknowledged

# Go into loop to watch messages
print(" [*] Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()
