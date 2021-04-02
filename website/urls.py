from django.urls import path
from django.conf.urls import url
from . import views 

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    url(r'^delete/(?P<id>.+?)/$', views.delete_contact, name="delete_contact"),
    path('inbox/', views.inbox, name='inbox'),
    path('terms_conditions/',views.terms_conditions, name="terms-conditions"),
    path('privacy_policy/',views.privacy_policy, name="privacy-policy"),
    path('cookie_policy/',views.cookie_policy, name="cookie-policy")
]
