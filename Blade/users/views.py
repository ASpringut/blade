
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from django.core.exceptions import ObjectDoesNotExist

from inventory.models import Resturant, Ingredient
from recipes.models import Recipe
#import user management models
from django.contrib.auth.models import User
from users.models import UserProfile


#import our forms
from users.InputForms import LoginForm, RegisterForm

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
    
    
    
    return render_to_response('login.html', render_dict)

    
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
            r = Resturant(name = form.cleaned_data['Resturant_Name'])
            r.save()
            
            #associate the user with their resturant
            user_prof = UserProfile(user=u,
                                    resturant = r)
            user_prof.save()
            
            return HttpResponse("Thanks for registering.")
        else:
            #if it failed add the errors to the render dictionary
            render_dict["errors"] = form.errors.__unicode__()
            
    #if this wasnt a request to register render the form
    render_dict["form"]=form
    render_dict.update(csrf(request))
    
    #display the form
    return render_to_response('register.html', render_dict, 
                              context_instance=RequestContext(request))
                              

def index(request):
    return render_to_response('index.html')
    

def resturantMain(request):
    
    if request.user.is_authenticated():
    
        render_dict = {}
        #get the resturant name
        key = request.user.id
        prof = UserProfile.objects.get(user=key)
        rest = prof.resturant
        #add the name of the resturant to be rendered
        render_dict["resturant_name"]=rest
        
        #get the first 10 ingredients
        try:
            #try to find ingredients for this resturant
            ingredient_list = list(Ingredient.objects.filter(resturant = rest.id))
        except ObjectDoesNotExist:
            ingredient_list=[]

        #get the first 10 recipes
        try:
            recipe_list = list(Recipe.objects.filter(resturant = rest.id))
        except ObjectDoesNotExist:
            recipe_list = []

        render_dict["recipes"] = recipe_list
        render_dict["ingredients"] = ingredient_list
        
        return render_to_response("main.html",render_dict)
            
        
    else:
        return HttpResponse("not logged in")