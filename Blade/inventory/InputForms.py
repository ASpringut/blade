from django.forms import Form, CharField, PasswordInput, EmailField, DecimalField, ModelChoiceField, ValidationError, Textarea, ModelForm
from inventory.models import Resturant, Ingredient
from Measures.models import Unit


    
class IngredientForm(Form):
    name = CharField(max_length=30)
    quantity = DecimalField()
    unit = ModelChoiceField(queryset=Unit.objects.all(),
							empty_label=None)
                            

    
