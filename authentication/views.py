from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegisterationSerializer,UserLoginSerializer,UserProfileSerializer,DoctorProfileSerializer
from django.contrib.auth import authenticate
from .tokens import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
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
     # def get(self,request,format=None):
     #      return Response({
     #           'msg':'Enter Your Credentials For Login',
     #           'fields':['email','password']
     #      },status=status.HTTP_200_OK)
     
     def post(self,request,format=None):
          serializer = UserLoginSerializer(data=request.data) 
          if serializer.is_valid():
               email = serializer.data.get('email') 
               password = serializer.data.get('password')
               user=authenticate(request,email=email,password=password)
               if user is not None:
                    if not user.blocked:
                         token = get_tokens_for_user(user)
                    else:
                         return Response({"msg":"Your Account is blocked"})
                    return Response({"msg":"Login Success","token":token},status=status.HTTP_200_OK)
               else:
                    return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
          return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
          
               
class UserProfileView(APIView):
     permission_classes = [IsAuthenticated]
     def get(self,request,pk=None,format=None):
          serializer = UserProfileSerializer(request.user)
          return Response(serializer.data,status=status.HTTP_200_OK)
     
     def put(self,request,pk=None,format=None):
          id=pk
          user = User.objects.get(id=id)
          if user.is_doctor:
               serializer = DoctorProfileSerializer(user,data=request.data,partial=True)
          else:
               serializer = UserProfileSerializer(user,data=request.data,partial=True)
          if serializer.is_valid():
               serializer.save()
               return Response({'msg':'Complete Data Updated'})
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
     
     def delete(self,request,pk=None,format=None):
          id = pk
          user = User.objects.get(pk=id)
          user.delete()
          return Response({'msg':'Data Deleted'},status=status.HTTP_200_OK)

          
class HomePageView(APIView):
     permission_classes = [IsAuthenticated]
     def get(self,request,format=None):
          user = User.objects.get(email=request.user)
          if not user.is_doctor and not user.is_admin:                      # For User
               doctors = User.objects.filter(is_doctor=True)
               serializer = DoctorProfileSerializer(doctors,many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)
          if user.is_doctor:                                                # For Doctor
               serializer = DoctorProfileSerializer(request.user)
               return Response(serializer.data,status=status.HTTP_200_OK)

               
          
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"detail": "Refresh token not provided."},status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)                    
        except Exception as e:
            return Response({"detail": "Invalid refresh token."},status=status.HTTP_400_BAD_REQUEST)
                            
          