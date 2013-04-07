from django.forms import Form, CharField, PasswordInput, EmailField, DecimalField, ModelChoiceField, ValidationError, Textarea, ModelForm
from inventory.models import Resturant, Ingredient, Recipe, RecipeIngredient
from Measures.models import Unit


class RegisterForm(Form):
    username = CharField(max_length=30)
    Password = CharField(widget=PasswordInput())
    Repeat_Password = CharField(widget= PasswordInput())
    Resturant_Name = CharField()
    E_mail = EmailField(label='E-mail')
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        
        pass1 = cleaned_data.get('Password')
        pass2 = cleaned_data.get('Repeat_Password')
        
        #check that passwords match
        if pass1 and pass2:
            if pass1 != pass2:
                raise ValidationError("Passwords do not match.")
        
        rest = cleaned_data.get('Resturant_Name')
        #check that resturant does not already exist
        if rest:
            print(len(Resturant.objects.filter(name=rest)))
            if len(Resturant.objects.filter(name=rest))!=0:
                raise ValidationError("Resturant already exists.")
    
        # Always return the full collection of cleaned data.
        return cleaned_data
        
class LoginForm(Form):
    username = CharField(max_length=30)
    Password = CharField(widget=PasswordInput())
    
    
class IngredientForm(Form):
    name = CharField(max_length=30)
    quantity = DecimalField()
    unit = ModelChoiceField(queryset=Unit.objects.all(),
							empty_label=None)
                            

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ('resturant',)
        widgets = {'instruction': Textarea()}
        
        
class RecipeIngredientForm(ModelForm):
    class Meta:
        model = RecipeIngredient
        exclude = ('recipe',)
    
