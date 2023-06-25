import pika
import os

# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

# connect to rabbitmq
connection = pika.BlockingConnection(url_params)
channel = connection.channel()

# declare a new queue
# durable flag is set so that messages are retained
# in the rabbitmq volume even between restarts
channel.queue_declare(queue='hello', durable=True)

for i in range(200, 250):
    channel.basic_publish(exchange='', routing_key='hello',
                       body=str(i), properties=pika.BasicProperties(delivery_mode=2))
    print("Produced the message")

channel.close()
connection.close()

# close the channel and connection
# to avoid program from entering with any lingering
# message in the queue cache