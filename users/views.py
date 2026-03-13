from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample

from .serializers import RegisterSerializer

# Create your views here.


@extend_schema(
    summary="User Registration",
    description="Create a new user account",
    request=RegisterSerializer,
    responses=RegisterSerializer,
    auth=False,
    methods=["POST"],
    examples=[
        OpenApiExample(
            "User Registration",
            value={
                "username": "testuser",
                "email": "testuser@gmail.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "password123",
            },
        )
    ],
)
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
