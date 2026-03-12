from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters

from rooms.serializers import RoomSerializer

from .models import Room

# Create your views here.


class FilterRoomsView(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_per_night", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price_per_night", lookup_expr="lte")
    min_capacity = filters.NumberFilter(field_name="capacity", lookup_expr="gte")
    max_capacity = filters.NumberFilter(field_name="capacity", lookup_expr="lte")

    class Meta:
        model = Room
        fields = ["room_number", "price_per_night", "capacity"]


class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = FilterRoomsView
    ordering_fields = ["price_per_night", "capacity"]