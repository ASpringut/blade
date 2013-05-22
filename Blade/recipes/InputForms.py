from django.forms import Textarea, ModelForm, Form
from recipes.models import Recipe, RecipeIngredient, RecipeService
from Measures.models import Unit

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ('restaurant', 'cost')
        widgets = {'instruction': Textarea()}
        
        
class RecipeIngredientForm(ModelForm):
    class Meta:
        model = RecipeIngredient
        exclude = ('recipe',)

class ServiceForm(ModelForm):
    class Meta:
        model = RecipeService
