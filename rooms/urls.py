from django.urls import path

from .views import ListRoomsView

urlpatterns = [
    path("", ListRoomsView.as_view(), name="list-rooms"),
]
