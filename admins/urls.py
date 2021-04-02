from django.urls import path
from admins import views
from django.conf.urls import url

urlpatterns = [

    path('view-customers/', views.view_customers, name="view-customers"),

]