from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('create-exam/', views.create_exam, name='create-exam'),
    path('view-exam/', views.view_exam, name='view-exam'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('edit-exam/<str:eid>', views.edit_exam, name='edit-exam'),
]
