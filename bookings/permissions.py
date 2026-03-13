from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View

from .models import Booking


class IsBookingOwnerOrSuperuser(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Booking) -> bool:
        if request.user.is_superuser:
            return True
        return obj.guest == request.user
