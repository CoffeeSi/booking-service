from django.db import models

# Create your models here.


class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True, db_index=True)
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, db_index=True
    )
    capacity = models.IntegerField()

    def __str__(self) -> str:
        return f"Room №{self.room_number}"
