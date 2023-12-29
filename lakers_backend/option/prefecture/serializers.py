from rest_framework import serializers


class PrefectureResponseSerializer(
    serializers.Serializer
):  # pylint: disable=abstract-method
    id = serializers.IntegerField()
    name = serializers.CharField()
    prefecture_code = serializers.CharField()
