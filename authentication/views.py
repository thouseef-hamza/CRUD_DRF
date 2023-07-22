from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegisterationSerializer
# Create your views here.

class UserRegisterationView(APIView):
     def get(self,request,format=None):
          return Response({'msg':'Register Your Credentials','Fields':['first_name','last_name','email','username','password','password2']})
     
     def post(self,request,format=None):
          serializer = UserRegisterationSerializer(data=request.data)
          if serializer.is_valid():
               user = serializer.save()
               return Response({'msg':'Registeration Successfull'},status=status.HTTP_201_CREATED)
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
          
               