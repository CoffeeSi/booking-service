from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, OpenApiExample

from rooms.serializers import RoomSerializer

from .models import Room

# Create your views here.


class FilterRooms(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_per_night", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price_per_night", lookup_expr="lte")
    capacity = filters.NumberFilter(field_name="capacity", lookup_expr="exact")

    class Meta:
        model = Room
        fields = ["room_number", "price_per_night", "capacity"]


@extend_schema(
    summary="List Rooms",
    description="Get a list of all rooms",
    responses=RoomSerializer(many=True),
    auth=False,
    examples=[
        OpenApiExample(
            "List Rooms with Filters",
            value=[
                {
                    "id": 1,
                    "room_number": "101",
                    "price_per_night": 1900.00,
                    "capacity": 1,
                },
                {
                    "id": 2,
                    "room_number": "201",
                    "price_per_night": 150.00,
                    "capacity": 2,
                },
            ],
        )
    ],
)
class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = FilterRooms
    ordering_fields = ["price_per_night", "capacity"]
