import json
import redis
import pika
from consumer import publish

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


def callback(ch, method, properties, body):
    data = json.loads(body)
    if properties.content_type == 'dictionary_created':
        key = data.get('key')
        value = data.get('value')
        redis_client.set(key, value, 3600)
    elif properties.content_type == "get_value_by_key":
        key = data
        channel.queue_declare(queue=key, durable=True)
        value = redis_client.get(key)
        if value:
            publish('set_value', value.decode(), key)


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='dictionary_queue')

channel.basic_consume(
    queue='dictionary_queue',
    on_message_callback=callback,
    auto_ack=True,
)
print("Started Consuming...")
channel.start_consuming()
connection.close()
