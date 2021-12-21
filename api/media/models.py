from django.db import models

from ..constants.media_types import MEDIA_TYPES, IMAGE
from ..user.models import EndUser

# Create your models here.


class Media(models.Model):
    link = models.CharField(max_length=500)
    caption = models.CharField(max_length=1000)
    type = models.CharField(
        max_length=5, choices=MEDIA_TYPES, default=IMAGE)
    owner = models.ForeignKey(EndUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.caption}"
