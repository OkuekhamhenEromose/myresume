


# after installing djangorestframework and adding it in installed app of settings
from rest_framework import serializers
from . models import Profile
from django.contrib.auth.models import User

from . utils import SendMail
# serializers are used to convert complex data types like querysets and model instances to native python datatypes
# that can then be easily rendered into JSON, XML or other content types. They also handle deserialization, allowing parsed data to be converted back into complex types after validating the incoming data.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']#this is added to the fields created

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSerializer()
        fields = ['gender','profile_pix','fullname','phone']

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    class Meta:
        model = Profile
        fields = ['fullname','username','email','password1','password2','gender','phone','profile_pix']
    def validate(self,data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('password does not match')
        return data
    def create(self, validated_data):
        username = validated_data.pop('username')#(a)removing default username set by django 
        email = validated_data.pop('email')
        password = validated_data.pop('password1')

        user = User.objects.create_user(username=username,email=email,password=password)#(b)to the one that is typed

        profile = Profile.objects.create(
            user = user,
            fullname = validated_data['fullname'],
            phone = validated_data['phone'],
            gender = validated_data['gender'],
            profile_pix = validated_data.get('profile_pix')
        )
        SendMail(email)
        return profile
    
class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',required=False)
    email = serializers.EmailField(source='user.email',required=False)
    class Meta:
        model = Profile
        fields=['fullname','username','email','gender','phone','profile_pix']
    def update(self,instance,validated_data):
        user_data=validated_data.pop('user,{}')
        user=instance.user
        if 'username' in user_data:# username is not empty
            user.username=user_data['username']
        if 'email' in user_data:
            user.email=user_data['email']
        user.save()

        instance.fullname = validated_data.get('fullname')
        instance.gender = validated_data.get('gender')
        instance.phone = validated_data.get('phone')
        instance.profile_pix = validated_data.get('profile_pix')
        instance.save()
        return instance
    