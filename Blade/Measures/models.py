from django.db import models

# Create your models here.
class Unit(models.Model):
	#the name of the unit
	name = models.CharField(max_length = 50)
	#the type of quantity being measured i.e. (w(eight), v(olume))
	type = models.CharField(max_length = 1)
	#the number to multiply to get to the base unit for the type
	#base unit is always the SI standard base unit e.g. 1000 for kilogram
	factor = models.FloatField()
	#abbreviation for the unit
	abbv = models.CharField(max_length = 10)
	
	def __unicode__(self):
		return self.name