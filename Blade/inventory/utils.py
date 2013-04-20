from users.models import UserProfile
from inventory.models import Ingredient
from django.core.exceptions import ObjectDoesNotExist
from decimal import *

#given a request get the restaurant name of the user
def get_rest(request):
    key = request.user.id
    prof = UserProfile.objects.get(user=key)
    rest = prof.restaurant
    return rest

#pass in a form that has already been checked for valididty
def add_ingredient(rest, form):

	try:
		name = form.cleaned_data['name']
		amount = form.cleaned_data['amount']
		unit = form.cleaned_data['unit']
		cost_per_unit = form.cleaned_data['cost_per_unit']
		#check to see if we already have an ingredient with that name
		db_ingredient = Ingredient.objects.get(name = name, restaurant =rest)

		#convert the given amount to the unit in the db
		converted_amount = amount*Decimal(unit.factor)/Decimal(db_ingredient.unit.factor)                        
		#add the amount to the database
		db_ingredient.amount = db_ingredient.amount + converted_amount
		#update the cost_per_unit to the new value
		db_ingredient.cost_per_unit = cost_per_unit
		db_ingredient.save()

	#if we get a does not exist error there isnt an ingredient by that name yet
	#so make a new one
	except ObjectDoesNotExist:
		ingredient = form.save(commit = False)
		ingredient.restaurant = rest
		ingredient.save()

	#it is possible to have blank rows if we got the form from a formset
	#if this happens we get a key error
	except KeyError:
		#there is nothing we need to do for a blank row
		pass