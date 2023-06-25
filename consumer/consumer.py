import pika
import requests
import time
import os
import json
import asyncio
from rds_connector import RDSConnector



amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)


connection = pika.BlockingConnection(url_params)
chan = connection.channel()

print(amqp_url)

chan.queue_declare(queue='hello', durable=True)

async def sla(dict):
    # Connect to RDS
    rds = RDSConnector()
    await rds.connect()
    retorno = await rds.create_data(
        data={
        'iseven': dict['iseven'],
        'ad': dict['ad'],
    })
    return retorno

def callback(ch, method, properties, body):
    time.sleep(2)
    print('acking it')
    chan.basic_ack(delivery_tag=method.delivery_tag)
    print("Received message: {}".format(body.decode("utf-8")))
    url_da_api = "https://api.isevenapi.xyz/api/iseven/" + body.decode("utf-8") + "/"
    response = requests.get(url_da_api)
    print("response: {}".format(response.content))
    dict = json.loads(response.content)
    print("dict iseven?: {}".format(dict['iseven']))

    test_data = asyncio.run(sla(dict))
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # test_data = loop.run_until_complete(sla(dict))

    print("test_data_id: {}".format(test_data.id))
    print("test_data_is_even: {}".format(test_data.iseven))

chan.basic_qos(prefetch_count=1)

# define the queue consumption
chan.basic_consume(queue='hello',
                   on_message_callback=callback)

print("Waiting to consume")
# start consuming
chan.start_consuming()

# rds.disconnect()