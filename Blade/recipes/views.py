from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory 
from django.forms.models import inlineformset_factory, modelformset_factory
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django_tables2 import RequestConfig

from recipes.InputForms import RecipeForm, RecipeIngredientForm, ServiceForm
from recipes.tables import ServiceTable

from inventory.models import Ingredient
from recipes.models import Recipe, RecipeIngredient, RecipeService


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
    ing_formset = RecipeIngredientFormset()

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


    #before the form is added to the render dict change the query set so the user
    #sees only their own ingredients
    user_ingredients = Ingredient.objects.filter(restaurant = rest)
    for form in ing_formset:
        form.fields['ingredient'].queryset=user_ingredients

    #add forms and csrf to dict
    render_dict['recipeform'] = recipeform
    render_dict['ingredientform'] = ing_formset
    render_dict.update(csrf(request))
    
        
    return render_to_response("add_recipe.html",
                              render_dict,
                              context_instance=RequestContext(request))
        


@login_required
def view_recipes(request):

    render_dict = {}

    #get the restaurant
    rest = InventoryUtils.get_rest(request)
    #add the restaurant to the render dictionary
    render_dict["restaurant_name"]= rest

    if request.method == "POST":
        #the only form on the page is the delete form, delete the requested recipes
        utils.delete_recipe(rest,request.POST)

    #get the recipes to display and add them to the renderdict
    try:
        recipe_list = list(Recipe.objects.filter(restaurant = rest.id))
    except ObjectDoesNotExist:
        recipe_list=[]

    render_dict["recipes"] = recipe_list
    #add the csrf form for deleting recipes
    render_dict.update(csrf(request))

    return render_to_response("view_recipes.html",
                              render_dict,
                              context_instance=RequestContext(request))

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

    #add the recipe to the render dict
    render_dict['recipe'] = recipe

    return render_to_response("view_recipe.html",
                              render_dict,
                              context_instance=RequestContext(request))


@login_required
def serve_recipe(request):

    render_dict = {}
    #get the restaurant
    rest = InventoryUtils.get_rest(request)

    # create the formset and add the form
    ServiceFormSet = modelformset_factory(RecipeService, extra=3)
    formset = ServiceFormSet(queryset=RecipeService.objects.none())

    #add the queryset so that users can only see their own recipes
    valid_recipes = Recipe.objects.filter(restaurant = rest)
    for form in formset:
        form.fields['recipe'].queryset = valid_recipes

    

    if request.method == "POST":
        formset = ServiceFormSet(request.POST)
        #if check for validity
        if formset.is_valid():
            print 'test'
            #save the forms
            formset.save()
            #clear the formset
            formset = ServiceFormSet(queryset=RecipeService.objects.none())
            #redirect to prevent resubmission
            return redirect(serve_recipe)


    #add the formset
    render_dict['formset'] = formset
    #add the csrf token
    render_dict.update(csrf(request))

    return render_to_response("serve_recipe.html",
                              render_dict,
                              context_instance=RequestContext(request))

@login_required
def view_service(request):

    render_dict={}

    #get the restaurant
    rest = InventoryUtils.get_rest(request)
    render_dict['restaurant'] = rest

    #get the services of all recipes belonging to the current user
    try:
        service_list = RecipeService.objects.filter(recipe__restaurant__pk=rest.id)
    except ObjectDoesNotExist:
        service_list = []

    #make the table of services
    table = ServiceTable(service_list)
    RequestConfig(request).configure(table)

    render_dict['table'] = table


    return render_to_response("view_service.html",
                              render_dict,
                              context_instance=RequestContext(request))
