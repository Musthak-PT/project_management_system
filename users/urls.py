from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    
    #Create, login and logout of users
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('create-or-update-user/', views.CreateOrUpdateUserApiView.as_view()),
    
    

]