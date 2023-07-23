from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.UserRegisterationView.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('profile/<int:pk>/',views.UserProfileView.as_view(),name='profile'),
    path('home/',views.HomePageView.as_view(),name='home'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),   
]
