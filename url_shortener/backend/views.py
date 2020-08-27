from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

@api_view(['POST'])
def generate_short_url(request):
    serializer = ShortURLSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    obj = serializer.save()

    response = {
        "id": str(obj),
        "link": request.build_absolute_uri(obj.get_absolute_url())
    }

    return Response(response, status=status.HTTP_201_CREATED)

def index(request):
    return HttpResponse("hello")

def redirect_to_long_url(request, short_url_id, *args, **kwargs):
    obj = get_object_or_404(ShortURLModel, pk=short_url_id)
    obj.access_counter += 1
    obj.save()

    if (obj.expiration_datetime < timezone.now() or
        obj.access_counter > obj.access_limit
    ):
        obj.delete()
        raise Http404

    return redirect(obj.long_url)