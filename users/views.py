
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

#import misceleneous models
from inventory.models import Restaurant, Ingredient
from recipes.models import Recipe
from service.models import RecipeService

#import user management models
from django.contrib.auth.models import User
from users.models import UserProfile

#import our forms
from users.InputForms import LoginForm, RegisterForm

from datetime import datetime, date, timedelta

# Create your views here.
def login_view(request):
    render_dict = {}
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['Password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse("Account Disabled")
            else:
                return HttpResponse("Incorrect login")
        
    #if this wasnt a request to register render the form
    render_dict["form"]=form
    render_dict.update(csrf(request))
    
    
    
    return render_to_response('login.html', 
                              render_dict,
                              context_instance=RequestContext(request))

    
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')
    
def register(request):

    #prepare the dict of values to render
    render_dict = {}
    #create the form early so it can be replaced if a form 
    #comes back bad
    form = RegisterForm()
    
    if request.method == 'POST': # If the form has been submitted...
        form=RegisterForm(request.POST)
        if form.is_valid():
            #if everything was filled out correctly 
            #create a user entry and save it
            u = User.objects.create_user(form.cleaned_data['username'],
                                            form.cleaned_data['E_mail'],
                                            form.cleaned_data['Password'])
                                            
            #create a new resutrant, no danger of doubles as we already checked 
            r = Restaurant(name = form.cleaned_data['Restaurant_Name'])
            r.save()
            
            #associate the user with their restaurant
            user_prof = UserProfile(user=u,
                                    restaurant = r)
            user_prof.save()
            user = authenticate(username=form.cleaned_data['username'], 
                                password=form.cleaned_data['Password'])
            if user is not None:
                login(request, user)
            return redirect(index)
        else:
            #if it failed add the errors to the render dictionary
            render_dict["errors"] = form.errors.__unicode__()
            
    #if this wasnt a request to register render the form
    render_dict["form"]=form
    render_dict.update(csrf(request))
    
    #display the form
    return render_to_response('register.html', 
                              render_dict, 
                              context_instance=RequestContext(request))
                              

def index(request):
    render_dict=[]
    return render_to_response('index.html',
                              render_dict,
                              context_instance=RequestContext(request))
   
@login_required
def restaurantMain(request):
    
    render_dict = {}
    #get the restaurant name
    key = request.user.id
    prof = UserProfile.objects.get(user=key)
    rest = prof.restaurant
    #add the name of the restaurant to be rendered
    render_dict["restaurant_name"]=rest
    
    #get the first 5 ingredients
    try:
        #try to find ingredients for this restaurant
        ing_list = Ingredient.objects
        ing_list = ing_list.filter(restaurant = rest.id)
        ing_list = ing_list.order_by("-date_modified")
        ing_list = list(ing_list[:5])
    except ObjectDoesNotExist:
        ingredient_list=[]
    render_dict["ingredients"] = ing_list

    #get the first 10 recipes
    try:
        recipe_list = Recipe.objects
        recipe_list = recipe_list.filter(restaurant = rest.id)
        recipe_list = recipe_list.order_by("-date_modified")
        recipe_list = list(recipe_list[:5])
    except ObjectDoesNotExist:
        recipe_list = []

    render_dict["recipes"] = recipe_list

    #dictionary of services by day
    day_list =[]
    #get todays date
    today = date.today()
    #for the last five days
    for i in range(5):
        td = timedelta(days=-1*i)
        day = today - td

        #get all of the services by day
        try:
            service_list = RecipeService.objects.filter(recipe__restaurant=rest.id)
            service_list = service_list.filter(date = day)
            #add a list of the day and the services
            day_list.append((day.strftime('%A'), list(service_list)))
        except ObjectDoesNotExist:
            day_list.append((day.strftime('%A'), []))

    render_dict['dayservice']=day_list

    
    return render_to_response("main.html",
                              render_dict,
                              context_instance=RequestContext(request))

def questions(request):
        render_dict={}
        return render_to_response("faq.html",
                              render_dict,
                              context_instance=RequestContext(request))
