from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import string
import random

class ShortURLModel(models.Model):
    def generate_expiration_datetime():
        return timezone.now() + timedelta(days=360)

    def generate_short_url_id():
        letters = list(string.ascii_letters)
        digits = [x for x in range(10)]
        values = letters + digits

        # 62^8 values
        id_ = "".join([str(random.choice(values)) for _ in range(8)])

        return id_
    
    short_url_id = models.CharField(
        primary_key=True,
        max_length=8,
        default=generate_short_url_id,
        editable=False
    )
    expiration_datetime = models.DateTimeField(
        default=generate_expiration_datetime
    )
    long_url = models.URLField()
    access_limit = models.PositiveSmallIntegerField(default=100)
    access_counter = models.PositiveSmallIntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def created_at_formated(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        return reverse(
            'backend:redirect_to_long_url', 
            kwargs={'short_url_id':self.short_url_id}
        )

    def __str__(self):
        return str(self.short_url_id)

    class Meta:
        db_table = 'vilantis_short_urls'
        verbose_name = 'short url'
        indexes = [models.Index(fields=['short_url_id']),]

class ClickStatisticModel(models.Model):
    short_url = models.ForeignKey(
        ShortURLModel,
        on_delete=models.CASCADE,
        editable=False
    )
    time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(editable=False)
    http_referer = models.URLField(editable=False, null=True, blank=True)

    def time_formatted(self):
        return self.time.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return str(self.short_url)

    class Meta:
        db_table = 'vilantis_short_url_click_statistics'
        verbose_name = 'short url statistic'
        indexes = [models.Index(fields=['short_url']),]