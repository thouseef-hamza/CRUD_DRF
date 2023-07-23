from django.urls import path
from . import views
urlpatterns = [
    path('user/',views.UserListAdminView.as_view(),name='user'),
    path('doctor/',views.DoctorListAdminView.as_view(),name='user'),
    path('user/update/<int:pk>/',views.UserProfileAdminView.as_view(),name='user'),
    path('doctor/update/<int:pk>/',views.DoctorProfileAdminView.as_view(),name='user'),
]
