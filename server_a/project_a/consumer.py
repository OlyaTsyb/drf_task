import json
import pika


def publish(method, body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='',
        routing_key='dictionary_queue',
        body=json.dumps(body),
        properties=properties
    )
    connection.close()
