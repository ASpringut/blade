from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

#import user management models
from django.contrib.auth.models import User
from users.models import UserProfile


from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from inventory.models import Restaurant, Ingredient
from recipes.models import Recipe
from inventory.InputForms import IngredientForm
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required

#import our general utility functions
import inventory.utils as utils

        
@login_required
def ingredient(request):

    render_dict = {}
    #get the restaurant
    rest = utils.get_rest(request)
    #add the restaurant to the render dictionary
    render_dict["restaurant_name"]= rest
    
    
    #create the form early so it can be replaced if a form 
    #comes back bad
    form = IngredientForm()
    

    #Deal with the ingredient add form
    if request.method == 'POST': # If the form has been submitted...
        #if the quickadd form was submitted
        if "quickadd" in request.POST:
            form=IngredientForm(request.POST)
            if form.is_valid():          
                utils.add_ingredient(rest, form)
                #return to page after redirect
                return redirect(ingredient_redirect)
        
        #if the delete form was submitted
        elif "delete" in request.POST:
            utils.delete_ingredients(rest, request.POST)


    #get the first 10 ingredients to display and add them to the renderdict
    try:
        #try to find ingredients for this restaurant
        ingred = list(Ingredient.objects.filter(restaurant = rest.id))

    #if the object does not exist there are not any ingredients 
    except ObjectDoesNotExist:
        ingred = []
        
    render_dict["ingredients"] = ingred  

    #add the form to the render dictionary
    render_dict["form"]=form
    render_dict.update(csrf(request))

    return render_to_response("ingredient.html",render_dict)
        
@login_required
def add_ingredients(request):
    render_dict = {}
    #get the restaurant
    rest = utils.get_rest(request)
    #add the restaurant to the render dictionary
    render_dict["restaurant_name"]= rest
    

    #create a formset, no restaurant because we should set that based
    #on the current login, also you dont want users touching other users'
    #restaurants
    IngredientFormset = modelformset_factory(Ingredient, 
                                             exclude=('restaurant',),
                                             extra=5)

    #this page should be for adding ingredients only
    formset = IngredientFormset(queryset=Ingredient.objects.none())

    if request.method == 'POST':
        formset = IngredientFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                utils.add_ingredient(rest, form)

            #if everything is valid we are done and should redirect back to
            #the viewing page
            return redirect(ingredient)

    
    render_dict['formset'] = formset
    render_dict.update(csrf(request))

    #create a formset for ingredients
    return render_to_response('add_ingredients.html', render_dict)

#page to return that immediately redirects to ingredient to hide POST data
#submission from the user
def ingredient_redirect(request):
    return redirect(ingredient)
