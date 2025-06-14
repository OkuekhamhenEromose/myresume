
from rest_framework import serializers
from .models import *

GENDER_CHOICES = [
 ('Male', 'Male'),
 ('Female', 'Female')
]

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resume
        fields='__all__'


class UserListingSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserListing
        fields='__all__'

class SingleListingSerializer(serializers.ModelSerializer):
    class Meta:
        model=SingleListing
        fields='__all__'