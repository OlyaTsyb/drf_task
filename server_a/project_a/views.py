from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .consumer import publish
from .serializers import DictionarySerializer
import pika
import json


class DictionaryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        key = kwargs.get('key')
        if key:
            publish('get_value_by_key', key)
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue=key, durable=True)
            while True:
                method_frame, header_frame, body = channel.basic_get(queue=key)
                if body:
                    value = json.loads(body)
                    channel.basic_ack(method_frame.delivery_tag)
                    channel.queue_delete(queue=key)
                    connection.close()
                    return Response(
                        {'message': f'Value {value} retrieved from Redis through server B'})
        else:
            return Response({'message': f'Neither was found'})

    def put(self, request):
        serializer = DictionarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        publish('dictionary_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
