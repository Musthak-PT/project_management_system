from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    
    #CRUD operations of tasks
    path('listing-of-tasks/', views.TaskListingApiView.as_view(), name='listing-task'),
    path('create-or-update-tasks/', views.CreateOrUpdateTasksApiView.as_view(), name='create-or-update-tasks'),
    path('delete-tasks/', views.DeleteTasksApiView.as_view(),name='delete-tasks'),
    
    #Endpoint to assign tasks to users
    path('assign-tasks/', views.AssignTasksApiView.as_view(), name='assign-tasks'),
    
]
