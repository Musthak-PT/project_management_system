from django.urls import path
from .views import NotificationViewSet
from . import views

app_name = 'notifications'

urlpatterns = [
      
    path('listing/', views.NotificationViewSet.as_view(), name='listing-notifications'),
    
]