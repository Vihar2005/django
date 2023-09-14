from django.shortcuts import render
from rest_framework import generics
from .models import Country
from .serializers import CountrySerializer
# Create your views here.


class CountryList(generics.ListCreateAPIView):
	queryset=Country.objects.all()
	serializer_class=CountrySerializer

class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=Country
	serializer_class=CountrySerializer
