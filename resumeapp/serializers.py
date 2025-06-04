
from rest_framework import serializers
from .models import *

GENDER_CHOICES = [
 ('Male', 'Male'),
 ('Female', 'Female')
]

JOB_CITY_CHOICE = [
 ('Delhi', 'Delhi'),
 ('Pune', 'Pune'),
 ('Ranchi', 'Ranchi'),
 ('Mumbai', 'Mumbai'),
 ('Dhanbad', 'Dhanbad'),
 ('Banglore', 'Banglore')
]

class ResumeSerializer(serializers.ModelSerializer):
 gender = serializers.ChoiceField(choices=GENDER_CHOICES, widget=serializers.RadioSelect)
 job_city = serializers.MultipleChoiceField(label='Preferred Job Locations', choices=JOB_CITY_CHOICE, widget=serializers.CheckboxSelectMultiple)
 class Meta:
  model = Resume
  fields = ['name', 'dob', 'gender', 'locality', 'city', 'pin', 'state', 'mobile', 'email', 'job_city', 'profile_image', 'my_file']
  labels = {'name':'Full Name', 'dob': 'Date of Birth', 'pin':'Pin Code', 'mobile':'Mobile No.', 'email':'Email ID', 'profile_image':'Profile Image', 'my_file':'Document'}
  widgets = {
   'name':serializers.TextInput(attrs={'class':'form-control'}),
   'dob':serializers.DateInput(attrs={'class':'form-control', 'id':'datepicker'}),
   'locality':serializers.TextInput(attrs={'class':'form-control'}),
   'city':serializers.TextInput(attrs={'class':'form-control'}),
   'pin':serializers.NumberInput(attrs={'class':'form-control'}),
   'state':serializers.Select(attrs={'class':'form-select'}),
   'mobile':serializers.NumberInput(attrs={'class':'form-control'}),
   'email':serializers.EmailInput(attrs={'class':'form-control'}),
  }


class UserListingSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserListing
        fields='__all__'

class SingleListingSerializer(serializers.ModelSerializer):
    class Meta:
        model=SingleListing
        fields='__all__'