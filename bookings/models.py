from django.db import models
from django.utils import timezone
from django.forms import ValidationError

# Create your models here.


class Booking(models.Model):
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)

    def clean(self) -> None:
        if not self.room or not self.guest:
            raise ValidationError("Room and guest must be specified")
        if self.start_date is None or self.end_date is None:
            raise ValidationError("Start date and end date must be specified")
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")
        if self.start_date < timezone.now().date():
            raise ValidationError("Start date cannot be in the past")

        if (
            Booking.objects.filter(
                room=self.room,
                start_date__lt=self.end_date,
                end_date__gt=self.start_date,
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError("This room is not available for the selected dates")

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=["start_date", "end_date"], name="booking_dates_index"),
        ]

    def __str__(self) -> str:
        return f"Booking {self.room} | Guest {self.guest.username} | {self.start_date} – {self.end_date}"
