from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render_to_response, redirect


from recipes.InputForms import RecipeForm, RecipeIngredientForm

from inventory.models import Ingredient
from recipes.models import Recipe, RecipeIngredient

#import our general utility functions
import inventory.InventoryUtils as InventoryUtils

@login_required       
def add_recipe(request):
    render_dict = {}
    
    #get the resturant
    rest = InventoryUtils.get_rest(request)
    #add the resturant to the render dictionary
    render_dict["resturant_name"]= rest
    
    #create the form
    recipeform = RecipeForm()
    RecipeIngredientFormset = formset_factory(RecipeIngredientForm)
    ing_formset = RecipeIngredientFormset();

    if request.method == 'POST': # If the form has been submitted...

        #parse the recipe form
        recipeform = RecipeForm(request.POST)
        ing_formset = RecipeIngredientFormset(request.POST)

        if recipeform.is_valid() and ing_formset.is_valid():
            #add the resaurant then save to the db
            recipe = recipeform.save(commit = False)
            recipe.resturant = rest
            recipe.save()
            
            #add all of the ingredients to the db
            for form in ing_formset:
                ingredient = form.save(commit = False)
                ingredient.recipe = recipe
                #dont save if the form is empty
                #there is no recipe if the amount is empty
                if ingredient.amount:
                    print('saving')
                    ingredient.save()

            #replace th forms with new ones so we dont see the same data again
            ing_formset = RecipeIngredientFormset()
            recipeform = RecipeForm()

            #redirect to the version of this page but without the post data
            #this prevents the user from accidentally refreshing
            #and submitting the form twice
            return redirect(add_recipe)


            
        else:
            print(recipeform.errors)
            print(ing_formset.errors)
            
    #add forms and csrf to dict
    render_dict['recipeform'] = recipeform
    render_dict['ingredientform'] = ing_formset
    render_dict.update(csrf(request))
    
        
    return render_to_response("recipes.html",render_dict)
        


@login_required
def view_recipes(request):

    render_dict = {}

    #get the resturant
    rest = InventoryUtils.get_rest(request)
    #add the resturant to the render dictionary
    render_dict["restaurant_name"]= rest

    #get the first 10 recipes to display and add them to the renderdict
    try:
        recipe_list = list(Recipe.objects.filter(resturant = rest.id))
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


    #get the resturant
    rest = InventoryUtils.get_rest(request)
    #add the resturant to the render dictionary
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
