from django.db import models
from django.utils import timezone
from django.forms import ValidationError

# Create your models here.


class Booking(models.Model):
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    guest = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if not self.room or not self.guest:
            raise ValidationError("Room and guest must be specified")
        if self.start_date is None or self.end_date is None:
            raise ValidationError("Start date and end date must be specified")
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")
        if self.start_date < timezone.now().date():
            raise ValidationError("Start date cannot be in the past")
        if Booking.objects.filter(
            room=self.room, start_date__lt=self.end_date, end_date__gt=self.start_date
        ).exists():
            raise ValidationError("This room is not available for the selected dates")

    def __str__(self):
        return f"Booking {self.room} | Guest {self.guest.username} | {self.start_date} – {self.end_date}"
