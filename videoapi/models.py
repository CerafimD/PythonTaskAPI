from django.db import models

# Create your models here.
import uuid
from django.db import models


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='videos/')
    filename = models.CharField(null=True, max_length=255)
    processing = models.BooleanField(default=False)
    processing_success = models.BooleanField(null=True, default=None)
