#import python types
from decimal import Decimal

#import django stuff
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django_tables2 import RequestConfig

#import stuff from other apps
from inventory import InventoryUtils
from recipes.models import Recipe

#import stuff from this app
from service.models import RecipeService
from service.tables import ServiceTable



@login_required
def serve_recipe(request):

    render_dict = {}
    #get the restaurant
    rest = InventoryUtils.get_rest(request)

    # create the formset and add the form
    ServiceFormSet = modelformset_factory(RecipeService, 
                                          extra=3, 
                                          exclude =("cost_at_serve",
                                                    "recipe_cost_at_serve"))
    formset = ServiceFormSet(queryset=RecipeService.objects.none())

    #add the queryset so that users can only see their own recipes
    valid_recipes = Recipe.objects.filter(restaurant = rest)
    for form in formset:
        form.fields['recipe'].queryset = valid_recipes

    if request.method == "POST":
        formset = ServiceFormSet(request.POST)
        #if check for validity
        if formset.is_valid():
            service_list = formset.save(commit=False)
            #add the cost and then save
            for service in service_list:
                service.recipe_cost_at_serve = service.recipe.cost
                service.cost_at_serve = service.recipe.cost *  Decimal(service.number)
                service.save()

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
