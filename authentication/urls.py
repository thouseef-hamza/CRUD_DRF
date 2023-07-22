from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.UserRegisterationView.as_view(),name='register'),
    
]