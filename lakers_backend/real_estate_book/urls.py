from django.urls import path

from . import views

app_name = "real_estate_book"

urlpatterns = [
    path("feed", views.RealEstateReceptionBookFeedView.as_view()),
    path("import-status", views.RealEstateReceptionBookImportStatusView.as_view()),
]
