from inventory.models import Ingredient
from django.core.exceptions import ObjectDoesNotExist

def add_ingredient(rest, ingName, quantity, ingUnit):
    #if the ingredient already exists
    try:
        ing = Ingredient.objects.filter(resturant = rest.id).filter(name = ingName)[0]
        ing.amount = ing.amount + quantity
        ing.save()
                                    
    except IndexError:
        #create a new entry
        ing = Ingredient(resturant = rest,
                         name = ingName,
                         amount = quantity,
                         unit = ingUnit)
        ing.save()
    