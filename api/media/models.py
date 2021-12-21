from django.db import models
from django.core.validators import FileExtensionValidator
from ..constants.media_types import MEDIA_TYPES, IMAGE
from ..user.models import EndUser

# Create your models here.


class Media(models.Model):
    file = models.FileField(upload_to='', validators=[FileExtensionValidator(
        allowed_extensions=['mp4', 'jpeg', 'png', 'mp3', 'jpg'])])
    caption = models.CharField(max_length=1000)
    type = models.CharField(
        max_length=5, choices=MEDIA_TYPES, default=IMAGE)
    owner = models.ForeignKey(EndUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.caption}"
