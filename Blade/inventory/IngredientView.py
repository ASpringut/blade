from inventory.models import Ingredient, IngredientQuantity
from django.core.exceptions import ObjectDoesNotExist

def add_ingredient(rest, ingName, quantity, ingUnit):
    #if the ingredient already exists
    try:
        ing = Ingredient.objects.filter(resturant = rest.id).filter(name = ingName)[0]


                                    
    except IndexError:
        #create a new entry
        ing = Ingredient(resturant = rest,
                                name = ingName)
        ingredient.save()
    
    newQuant = IngredientQuantity(ingredient = ing,
                                  amount = quantity,
                                  unit = ingUnit)
    newQuant.save();