# RabbitMQ with Pika
This is how to use rabbitmq as message broker with python's pika client.

# How-to
1. ensure rabbitmq is installed in your local
2. code in `send.py` is a producer. It is used to publish message to queue.
3. code in `receive.py` is a consumer. It is used to receive and consume message in queue. It will be running endlessly in loop.
