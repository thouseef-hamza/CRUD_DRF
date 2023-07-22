from rest_framework import serializers
from .models import User
import re

class UserRegisterationSerializer(serializers.ModelSerializer):
     password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
     class Meta:
          model = User
          fields = ['first_name','last_name','username','email','password','password2']
          extra_kwargs = {
               'password':{'write_only':True}
          }
          
     
     # Object Level Validation
     def validate(self, attrs):
          password = attrs.get('password')
          password2 = attrs.get('password2')
          first_name = attrs.get('first_name')
          last_name = attrs.get('last_name')
          if first_name == last_name:
               raise serializers.ValidationError('First Name And Last Name Can\'t Be Same')
          if password != password2:
               raise serializers.ValidationError('Password Didn\'t Match')
          return attrs
     
     def create(self, validated_data):
          return User.objects.create_user(**validated_data)
     
class UserLoginSerializer(serializers.ModelSerializer):
     email = serializers.EmailField(max_length=255)
     class Meta:
          model = User
          fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id','first_name','last_name','username','email']