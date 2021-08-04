from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import Contact


class ContactSerializer(ModelSerializer):

    class Meta:
        model = Contact
        # fields = '__all__'
        fields = ['country_code', 'first_name', 'last_name', 'id',
                  'phone_number', 'picture_url', 'is_favorite']
