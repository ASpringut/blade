from django.forms import Form, ModelForm, CharField, PasswordInput, EmailField, DecimalField, ModelChoiceField, ValidationError, Textarea, ModelForm
from inventory.models import Restaurant, Ingredient
from Measures.models import Unit


    
class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        exclude = ('restaurant', 'date_modified', 'total_value')

    
