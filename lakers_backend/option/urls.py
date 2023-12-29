from django.urls import path

from .city import views as city_views
from .prefecture import views as prefecture_views
from .reception_reason import views as reception_reason_views

app_name = "option"

urlpatterns = [
    path("city", city_views.CityView.as_view()),
    path("reception-reason", reception_reason_views.ReceptionReasonView.as_view()),
    path("prefecture", prefecture_views.PrefectureView.as_view()),
]
