from rest_framework import serializers


class CityResponseSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    id = serializers.IntegerField()
    name = serializers.CharField()
    city_code = serializers.CharField()
    pref_code = serializers.CharField()
