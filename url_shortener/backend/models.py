from django.db import models
from django.urls import reverse
from datetime import datetime
from datetime import timedelta
import uuid

class ShortURLModel(models.Model):
    short_url_id = models.CharField(
        primary_key=True,
        max_length=8,
        default=uuid.uuid4().hex[:8],
        editable=False
    )
    long_url = models.URLField()
    expiration_datetime = models.DateTimeField(
        default=datetime.now() + timedelta(days=360)
    )
    access_limit = models.PositiveSmallIntegerField(default=100)
    access_counter = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('backend:redirect_to_long_url', kwargs={'short_url_id':self.short_url_id})

    def __str__(self):
        return self.short_url_id

    class Meta:
        db_table = 'vilantis_short_urls'