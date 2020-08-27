from django.urls import path
from .views import *

app_name = "backend"

urlpatterns = [
    path('', index, name='index'),
    path('<str:short_url_id>/',
        redirect_to_long_url,
        name='redirect_to_long_url'
    ),
    path('api/generate_url/',
        generate_short_url,
        name='generate_short_url'
    )
]