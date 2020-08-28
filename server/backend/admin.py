from django.contrib import admin
from .models import *

class ClickStatisticInline(admin.TabularInline):
    model = ClickStatisticModel
    readonly_fields = ('ip_address', 'time_formatted', 'http_referer')
    ordering = ['-time']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(ShortURLModel)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('short_url_id', 'long_url', 'is_active', 'created_at_formated')
    readonly_fields = ['short_url_id', 'access_counter', 'long_url']
    inlines = [ClickStatisticInline,]
    ordering = ['-created_at']