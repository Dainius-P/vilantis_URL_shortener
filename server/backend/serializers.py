from rest_framework import serializers
from .models import *

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURLModel
        fields = ['long_url', 'expiration_datetime', 'access_limit']