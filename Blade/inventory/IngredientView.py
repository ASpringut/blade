from inventory.models import Ingredient
from django.core.exceptions import ObjectDoesNotExist
from decimal import *
def add_ingredient(rest, ingName, quantity, ingUnit):
    #if the ingredient already exists
    try:
        ing = Ingredient.objects.filter(resturant = rest.id).filter(name = ingName)[0]
        
        #if these two units are compatible
        if ingUnit.type == ing.unit.type:
        
            #check to see if the unit is the same
            if ingUnit == ing.unit:
                #if it is we can simply add
                ing.amount = ing.amount + quantity
            #otherwise we must convert first and then add
            else:
                #convert the amount to be added to the base unit
                converted_amount = float(quantity) * ingUnit.factor
                #convert from the base unit to the unit already being used
                converted_amount = converted_amount / float(ing.unit.factor)
                
                ing.amount = Decimal(ing.amount) + Decimal(converted_amount)
            
            ing.save()
            
        #otherwise these units are incompatible
        else:
            #do nothing for now but later raise an error
            pass
            
    except IndexError:
        #create a new entry
        ing = Ingredient(resturant = rest,
                         name = ingName,
                         amount = quantity,
                         unit = ingUnit)
        ing.save()
    