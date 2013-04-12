from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, redirect


from recipes.InputForms import RecipeForm, RecipeIngredientForm

from inventory.models import Ingredient
from recipes.models import Recipe

#import our general utility functions
import inventory.InventoryUtils as InventoryUtils

@login_required       
def recipes(request):
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
            
        else:
            print(recipeform.errors)
            print(ing_formset.errors)
            
    #add forms and csrf to dict
    render_dict['recipeform'] = recipeform
    render_dict['ingredientform'] = ing_formset
    render_dict.update(csrf(request))

    #get the first 10 recipes to display and add them to the renderdict
    try:
        #try to find ingredients for this resturant
        recipe_list = list(Ingredient.objects.filter(resturant = rest.id))
    except ObjectDoesNotExist:
        recipe_list=[]
    render_dict["ingredients"] = recipe_list 
    
        
    return render_to_response("recipes.html",render_dict)
        
        
        
        
