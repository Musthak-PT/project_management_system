from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    
    #_______________________________CRUD Operations of projects_________________________________________________________
    
    path('listing-of-projects/', views.ProjectListingApiView.as_view(), name='listing-project'),
    path('create-or-update-projects/', views.CreateOrUpdateProjectsApiView.as_view(), name='create-or-update-project'),
    path('delete-projects/', views.DeleteProjectsApiView.as_view(),name='delete-project'),
    
]