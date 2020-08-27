from django.contrib import admin
from .models import *

@admin.register(ShortURLModel)
class ShortURLAdmin(admin.ModelAdmin):
    pass