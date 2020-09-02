from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
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
    # An instance of a newly saved short_url is stored 
    # so we could generate a Response
    obj = serializer.save()

    response = {
        "id": str(obj),
        "link": request.build_absolute_uri(obj.get_absolute_url()),
        "created": obj.created_at
    }

    return Response(response, status=status.HTTP_201_CREATED)

def redirect_to_long_url(request, short_url_id, *args, **kwargs):
    obj = get_object_or_404(ShortURLModel, pk=short_url_id)

    # Check if short url hasn't exceeded the maximum number of redirects and
    # if it is not expired
    if not obj.is_active:
        raise Http404
    elif(obj.expiration_datetime < timezone.now()):
        obj.is_active = False
        obj.save()
        raise Http404
    elif(obj.access_limit is not None and obj.access_limit < obj.access_counter):
        obj.is_active = False
        raise Http404

    obj.access_counter += 1
    obj.save()

    ClickStatisticModel.objects.create(
        short_url=obj,
        ip_address=request.META['REMOTE_ADDR'],
        http_referer=request.META.get('HTTP_REFERER')
    )

    return redirect(obj.long_url)