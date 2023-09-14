from django.db import models

# Create your models here.
class Country(models.Model):
	countryname=models.CharField(max_length=100,blank=True)
	population=models.CharField(max_length=100,blank=True)

	def __str__(self):
		return self.countryname
