import pika
import requests
import os
import json
import logging

from rds_connector import RDSConnector
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Starting consumer")

logging.info("Connecting to RabbitMQ")
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

connection = pika.BlockingConnection(url_params)
chan = connection.channel()

logging.info("Declaring queue")
chan.queue_declare(queue='hello', durable=True)

logging.info("Connecting to RDS")
rds = RDSConnector()
rds.connect()
logging.info("Connected to RDS")

def callback(ch, method, properties, body):
    
    try:
        ##informa ao RabbitMQ que a mensagem foi processada corretamente e pode ser removida da fila
        logging.info("Acking message")
        chan.basic_ack(delivery_tag=method.delivery_tag)
        
        logging.info("Received message: {}".format(body.decode("utf-8")))
        url_da_api = "https://api.isevenapi.xyz/api/iseven/" + body.decode("utf-8") + "/"
        logging.info("Calling API: {}".format(url_da_api))
        response = requests.get(url_da_api)
        logging.info("API response: {}".format(response.status_code))

        dict = json.loads(response.content)
        logging.info("dict: {}".format(dict))

        logging.info("Creating data")
        test_data = rds.create_data(
            data={
            'iseven': dict['iseven'],
            'ad': dict['ad'],
        })
        logging.info("Data created: id:{} is_even: {} ad: {}".format(test_data.id, test_data.iseven, test_data.ad))
        #rds.print_all()
        #print()
    except Exception as e:
        logging.error("Error: {}".format(e))
        logging.info("Nacking message")
        chan.basic_nack(delivery_tag=method.delivery_tag)
        logging.info("Message nacked")

logging.info("Declaring callback")
chan.basic_qos(prefetch_count=1)

chan.basic_consume(queue='hello',
                   on_message_callback=callback)
logging.info("Waiting to consume")

chan.start_consuming()

logging.info("RDS Closing connection")
rds.disconnect()
logging.info("RDS Connection closed")