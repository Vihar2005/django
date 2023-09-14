from django.urls import path
from . import views

urlpatterns = [
    path('', views.country_search, name= 'country_search'),
]
