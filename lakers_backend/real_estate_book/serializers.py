from rest_framework import serializers


class RealEstateReceptionBookFeedResponseSerializer(
    serializers.Serializer
):  # pylint: disable=abstract-method
    id = serializers.IntegerField()
    chiban = serializers.CharField()
    kaoku_number = serializers.CharField()
    real_estate_book_type_id = serializers.IntegerField()
    real_estate_book_type_name = serializers.CharField()
    reception_reason = serializers.CharField()
    real_estate_type_id = serializers.IntegerField()
    real_estate_type_name = serializers.CharField()
    is_new = serializers.BooleanField()
    prefectures_city_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    city_name = serializers.CharField()
    prefectures_id = serializers.IntegerField()
    prefectures_name = serializers.CharField()
    address = serializers.CharField()
    outside = serializers.CharField()
    legal_affairs_bureau_request_date = serializers.DateField()
    legal_affairs_bureau_reception_number = serializers.CharField()


class RealEstateReceptionBookImportStatusResponseSerializer(
    serializers.Serializer
):  # pylint: disable=abstract-method
    prefectures_id = serializers.IntegerField()
    prefectures_name = serializers.CharField()
    import_date = serializers.DateField(format="%Y-%m-%d")
    legal_affairs_bureau_request_month = serializers.DateField(format="%Y-%m")
