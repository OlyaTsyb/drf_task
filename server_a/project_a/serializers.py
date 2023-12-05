from rest_framework import serializers


class DictionarySerializer(serializers.Serializer):
    key = serializers.CharField(required=False)
    value = serializers.CharField(required=False)
