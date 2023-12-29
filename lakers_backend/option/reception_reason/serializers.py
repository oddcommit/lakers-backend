from rest_framework import serializers


class ReceptionReasonResponseSerializer(
    serializers.Serializer
):  # pylint: disable=abstract-method
    id = serializers.IntegerField()
    name = serializers.CharField()
