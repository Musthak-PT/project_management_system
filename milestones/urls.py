from django.urls import path
# from .views import MilestoneViewSet
from . import views

app_name = 'milestones'

urlpatterns = [
      
    #CRUD operations of milestones
    path('listing-of-milestones/', views.MilestoneListingApiView.as_view(), name='listing-milestone'),
    path('create-or-update-milestones/', views.CreateOrUpdateMilestoneApiView.as_view(), name='create-or-update-milestone'),
    path('delete-milestones/', views.DeleteMilestoneApiView.as_view(),name='delete-milestone'),  
]