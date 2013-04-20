from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render_to_response, redirect


from recipes.InputForms import RecipeForm, RecipeIngredientForm

from inventory.models import Ingredient
from recipes.models import Recipe, RecipeIngredient


#import our general utility functions
import inventory.utils as InventoryUtils
import recipes.utils as utils

@login_required       
def add_recipe(request):
    render_dict = {}
    
    #get the restaurant
    rest = InventoryUtils.get_rest(request)
    #add the restaurant to the render dictionary
    render_dict["restaurant_name"]= rest
    
    #create the form
    recipeform = RecipeForm()
    RecipeIngredientFormset = inlineformset_factory(Recipe, RecipeIngredient)
    ing_formset = RecipeIngredientFormset();

    #if we receive information about a recipe to load
    if request.method == 'GET' and 'recipe' in request.GET:

        #get the recipe being requested
        recipe_key = request.GET['recipe']
        recipe = Recipe.objects.get(id = recipe_key)
        #load the recipe into the form
        recipeform = RecipeForm(instance = recipe)
        ing_formset = RecipeIngredientFormset(instance = recipe);

    # If the form has been submitted
    if request.method == 'POST':

        #if we have a recipe id we are editing an old model
        if 'recipe' in request.GET:
            recipe = Recipe.objects.get(id = request.GET['recipe'])
            print(recipe)
            #parse the recipe form
            recipeform = RecipeForm(request.POST, instance = recipe)
        #otherwise we are adding a new model
        else:
            recipeform = RecipeForm(request.POST)


        
        if recipeform.is_valid():

            #add the resaurant then temporarily save
            recipe = recipeform.save(commit = False)
            recipe.restaurant = rest
            recipe = recipeform.save()
            #create the formset with the recipe 
            ing_formset = RecipeIngredientFormset(request.POST,
                                                  instance = recipe)

            #if the formset is valid and therefore both are 
            #valid
            if ing_formset.is_valid():

                #once we know the full transaction is good
                #we can save the recipe to the database
                recipe.save()
                
                #and the ingredients
                ing_formset.save()

                #redirect to the version of this page but without the post data
                #this prevents the user from accidentally refreshing
                #and submitting the form twice
                return redirect(add_recipe)


            
    #add forms and csrf to dict
    render_dict['recipeform'] = recipeform
    render_dict['ingredientform'] = ing_formset
    render_dict.update(csrf(request))
    
        
    return render_to_response("add_recipe.html",render_dict)
        


@login_required
def view_recipes(request):

    render_dict = {}

    #get the restaurant
    rest = InventoryUtils.get_rest(request)
    #add the restaurant to the render dictionary
    render_dict["restaurant_name"]= rest

    #get the first 10 recipes to display and add them to the renderdict
    try:
        recipe_list = list(Recipe.objects.filter(restaurant = rest.id))
    except ObjectDoesNotExist:
        recipe_list=[]

    render_dict["recipes"] = recipe_list


    return render_to_response("view_recipes.html",render_dict)

@login_required
def view_recipe(request):

    render_dict = {}
    '''
    This page is built around viewing a single retreived 
    recipe. So if there is no request for one something has gone
    wrong. 
    '''
    if not 'recipe' in request.GET:
        #redirect to the recipes page
        return redirect(view_recipes)


    #get the restaurant
    rest = InventoryUtils.get_rest(request)
    #add the restaurant to the render dictionary
    render_dict["restaurant_name"]= rest

    try:
        #get the recipe being queried
        recipe = Recipe.objects.get(id = request.GET['recipe'])
    except ObjectDoesNotExist:
        return redirect(view_recipes)

    #get all of the ingredients
    ingredients = list(RecipeIngredient.objects.filter(recipe=recipe))
    render_dict["ingredients"] = ingredients

    #add it to the render dict
    render_dict['recipe'] = recipe

    return render_to_response("view_recipe.html",render_dict)
