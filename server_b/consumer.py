import json
import pika


def publish(method, body, key):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue=key, durable=True)
    properties = pika.BasicProperties(method)

    channel.basic_publish(
        exchange='',
        routing_key=f'{key}',
        body=json.dumps(body),
        properties=properties
    )
    connection.close()
