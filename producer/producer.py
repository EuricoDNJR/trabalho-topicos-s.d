import pika
import os

amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

connection = pika.BlockingConnection(url_params)
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)

for i in range(200, 250):
    channel.basic_publish(exchange='', routing_key='hello',
                       body=str(i), properties=pika.BasicProperties(delivery_mode=2))
    print("Produced the message")

channel.close()
connection.close()
