from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from authentication.models import User
from .serializers import UserProfileAdminSerializer,DoctorProfileAdminSerializer,UserListAdminSerializer,DoctorListAdminSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class UserListAdminView(APIView):
     # permission_classes=[IsAdminUser]
     
     def get(self, request,format=None):
          users = User.objects.filter(is_doctor=False,is_admin=False)
          serializer = UserListAdminSerializer(users, many=True)
          return Response(serializer.data)
     
class UserProfileAdminView(APIView):
     permission_classes=[IsAdminUser,IsAuthenticated]
     
     def get(self, request,pk=None,format=None):
          id =pk
          users = User.objects.get(pk=id)
          serializer = UserProfileAdminSerializer(users)
          return Response(serializer.data,status=status.HTTP_200_OK)
     
     def put(self, request,pk=None,format=None):
          id =pk
          users = User.objects.get(pk=id)
          serializer = UserProfileAdminSerializer(users,data=request.data,partial=True)
          if serializer.is_valid():
               serializer.save()
               return Response({"msg":"Data Updated "},status=status.HTTP_200_OK)
          return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
     
     def delete(self,request,pk=None,format=None):
          id = pk
          user = User.objects.get(pk=id)
          user.delete()
          return Response({'msg':'Data Deleted'})
     
class DoctorListAdminView(APIView):
     permission_classes=[IsAdminUser,IsAuthenticated]
     
     def get(self, request,format=None):
          users = User.objects.filter(is_doctor=True,is_admin=False)
          serializer = DoctorListAdminSerializer(users, many=True)
          return Response(serializer.data,status=status.HTTP_200_OK)

class DoctorProfileAdminView(APIView):
     permission_classes=[IsAdminUser,IsAuthenticated]
     
     def get(self, request,pk=None,format=None):
          users = User.objects.get(id=pk)
          serializer = DoctorProfileAdminSerializer(users)
          return Response(serializer.data)
     
     def put(self, request,pk=None,format=None):
          id =pk
          users = User.objects.get(pk=id)
          serializer = UserProfileAdminSerializer(users,data=request.data,partial=True)
          if serializer.is_valid():
               serializer.save()
               return Response({"msg":"Data Updated "},status=status.HTTP_200_OK)
          return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
     
     def delete(self,request,pk=None,format=None):
          id = pk
          user = User.objects.get(pk=id)
          user.delete()
          return Response({'msg':'Data Deleted'},status=status.HTTP_200_OK)