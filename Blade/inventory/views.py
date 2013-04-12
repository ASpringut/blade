from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

#import user management models
from django.contrib.auth.models import User
from users.models import UserProfile


from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from inventory.models import Resturant, Ingredient
from recipes.models import Recipe
from inventory.InputForms import IngredientForm

from django.contrib.auth.decorators import login_required

#import our general utility functions
import inventory.InventoryUtils as InventoryUtils
#import helper functions for viewing ingredients
import inventory.IngredientUtils as IngredientUtils


        
@login_required
def ingredient(request):

    render_dict = {}
    #get the resturant
    rest = InventoryUtils.get_rest(request)
    #add the resturant to the render dictionary
    render_dict["resturant_name"]= rest
    
    
    #create the form early so it can be replaced if a form 
    #comes back bad
    form = IngredientForm()
    

    #Deal with the ingredient add form
    if request.method == 'POST': # If the form has been submitted...
        form=IngredientForm(request.POST)
        if form.is_valid():
            
            IngredientUtils.add_ingredient(rest, 
                                          form.cleaned_data['name'],
                                          form.cleaned_data['quantity'],
                                          form.cleaned_data['unit'])
        
        else:
            #if it failed add the errors to the render dictionary
            render_dict["errors"] = form.errors.__unicode__()

            
            
    #get the first 10 ingredients to display and add them to the renderdict
    try:
        #try to find ingredients for this resturant
        ingred = list(Ingredient.objects.filter(resturant = rest.id))
        #get the tuple form of the ingredients in a list
        quantities = [ing.to_tuple() for ing in ingred]

    #if the object does not exist there are not any ingredients 
    except ObjectDoesNotExist:
        quantities = []
        
    render_dict["ingredients"] = quantities  

    #add the form to the render dictionary
    render_dict["form"]=form
    render_dict.update(csrf(request))

    return render_to_response("ingredient.html",render_dict)
        
