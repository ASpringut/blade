from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

#import json for ajax requests
from django.utils import simplejson

from inventory.models import Ingredient
from Measures.models import Unit



'''
return a json list of ids for valid units given an id of an ingredient

a get request is made to this page with name = 'unit' and value = the id of the
ingredient to get units for
'''
def get_units(request):

    #get the ingredient id from the request
    ingredient_id = request.GET['ingredient']
    
    try:
        #look up the ingredient in the database
        ingredient = Ingredient.objects.get(id = ingredient_id)
        #get the type of the unit
        unit_type = ingredient.unit.type
        #get all the units with a matching type
        matching_units = Unit.objects.filter(type = unit_type)
        
    #if the object does not exists assume every unit is valid    
    except ObjectDoesNotExist:
        matching_units = Unit.objects.all()
    
    #make a list of the IDs of the matching units
    unit_id_list = [unit.id for unit in matching_units]
    #convert to json
    json = simplejson.dumps(unit_id_list)
    return HttpResponse(json, mimetype='application/json')
    