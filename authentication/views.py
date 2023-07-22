from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegisterationSerializer,UserLoginSerializer,UserProfileSerializer
from django.contrib.auth import authenticate
from .tokens import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UserRegisterationView(APIView):
     def get(self,request,format=None):
          return Response({
               'msg':'Register Your Credentials',
               'Fields':['first_name','last_name','email','username','password','password2']
          },status=status.HTTP_200_OK)
     
     def post(self,request,format=None):
          serializer = UserRegisterationSerializer(data=request.data)
          if serializer.is_valid():
               user = serializer.save()
               token = get_tokens_for_user(user)
               return Response({'msg':'Registeration Successfull','token':token},status=status.HTTP_201_CREATED)
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
     def get(self,request,format=None):
          return Response({
               'msg':'Enter Your Credentials For Login',
               'fields':['email','password']
          },status=status.HTTP_200_OK)
     
     def post(self,request,format=None):
          serializer = UserLoginSerializer(data=request.data) 
          if serializer.is_valid():
               email = serializer.data.get('email') 
               password = serializer.data.get('password')
               user=authenticate(email=email,password=password)
               if user is not None:
                    if user.blocked == False:
                         token = get_tokens_for_user(user)
                    else:
                         return Response({"msg":"Your Account is blocked"})
                    return Response({"msg":"Login Success","token":token},status=status.HTTP_200_OK)
               else:
                    return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
          return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
          
               
class UserProfileView(APIView):
     permission_classes = [IsAuthenticated]
     def get(self,request,format=None):
          serializer = UserProfileSerializer(request.user)
          return Response(serializer.data,status=status.HTTP_200_OK)

          
          
     
          