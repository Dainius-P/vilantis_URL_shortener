from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from .models import *

class AccountTests(APITestCase):
    def test_short_url(self):
        url = reverse('backend:generate_short_url')
        data = {"long_url": "http://example.com/"}

        # Generate short URL
        response = self.client.post(url, data, format='json')
        short_url_id = response.json()['id']

        short_url_obj = ShortURLModel.objects.get(pk=short_url_id)

        # Testing generating long URL to short URL
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(short_url_obj.short_url_id, short_url_id)

        redirect_response = self.client.get(
            reverse('backend:redirect_to_long_url', kwargs={
                'short_url_id':short_url_obj.short_url_id
            })
        )

        # Testing short URL redirect to long URL
        self.assertEqual(redirect_response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(redirect_response.url, short_url_obj.long_url)

    def test_very_long_url_to_short_url(self):
        url = reverse('api:generate_short_url')
        data = {"long_url": "https://www.google.com/maps/place/Kurtuv%C4%97nai+regional+park/@55.8124971,23.0073874,3a,75y,340h,90t/data=!3m8!1e1!3m6!1sAF1QipPwgVise_4lVEAMnHPegN2jijvHRTE-YeFGP6Cx!2e10!3e11!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2FAF1QipPwgVise_4lVEAMnHPegN2jijvHRTE-YeFGP6Cx%3Dw86-h86-k-no-pi0-ya298-ro-0-fo100!7i8000!8i4000!4m5!3m4!1s0x0:0x11c2fdac35593e03!8m2!3d55.8124971!4d23.0073873"}

        # Try to generate a short url from a very long URL
        response = self.client.post(url, data, format='json')

        # Testing if short url was not generated
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['long_url'][0], 
            "Ensure this field has no more than 200 characters."
        )

    def test_short_url_access_limit(self):
        url = reverse('backend:generate_short_url')
        data = {"long_url": "http://example.com/"}

        # Generate short URL
        response = self.client.post(url, data, format='json')
        short_url_id = response.json()['id']

        short_url_obj = ShortURLModel.objects.get(pk=short_url_id)
        short_url_obj.access_limit = 1
        short_url_obj.save()

        redirect_response = self.client.get(
            reverse('backend:redirect_to_long_url', kwargs={
                'short_url_id':short_url_obj.short_url_id
            })
        )

        short_url_obj = ShortURLModel.objects.get(pk=short_url_id)

        self.assertEqual(redirect_response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(short_url_obj.is_active, True)
        self.assertEqual(redirect_response.url, short_url_obj.long_url)

        redirect_response = self.client.get(
            reverse('backend:redirect_to_long_url', kwargs={
                'short_url_id':short_url_obj.short_url_id
            })
        )

        short_url_obj = ShortURLModel.objects.get(pk=short_url_id)

        self.assertEqual(redirect_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(short_url_obj.is_active, False)