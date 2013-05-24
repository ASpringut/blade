from users.models import UserProfile
from inventory.models import Ingredient
from recipes.models import Recipe, RecipeIngredient
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

        #determine the convert factor
        convert_factor = Decimal(unit.factor)/Decimal(db_ingredient.unit.factor)

        #convert the given amount to the unit in the db
        converted_amount = amount*convert_factor                     
        #add the amount to the database
        db_ingredient.amount = db_ingredient.amount + converted_amount

        converted_cpu = cost_per_unit/convert_factor
        #update the cost_per_unit to the new value
        db_ingredient.cost_per_unit = converted_cpu

        db_ingredient.save()
        #update any recipes that are dependent on the ingredient
        #we only need to do this for exisiting ingredients because you cant have a recipe with
        #an ingredient that has not been added yet
        update_recipes(db_ingredient)

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

#pass in the post dict of the request
def delete_ingredients(rest, post):
    delete_list = post.getlist('delete')
    #convert the list to ingredient objects 
    delete_list = [Ingredient.objects.get(pk=int(ing_id)) for ing_id in delete_list]
    for ing in delete_list:
        #check if the ingredient belongs to the restaurant of the current user
        if (ing.restaurant == rest):
            #delete the ingredients
            ing.delete()            

#re-saves the recipes that are dependent on an ingredient
#so that their cost column is updated
def update_recipes(changed_ing):
    #do a reverse lookup from foreign key
    update_rec_ings = RecipeIngredient.objects.filter(ingredient = changed_ing)
    rec_ing_id = update_rec_ings.values_list('id', flat=True)
    update_rec = Recipe.objects.filter(id__in=rec_ing_id)

    #save all the recipes to update prices
    for rec in update_rec:
        rec.save()