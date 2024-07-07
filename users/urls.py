from django.urls import path
from .views import UserViewSet
from . import views

app_name = 'users'

urlpatterns = [
      
    path('listing/', views.UserViewSet.as_view(), name='listing-users'),
    
]