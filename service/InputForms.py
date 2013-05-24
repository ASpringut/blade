from django.forms import ModelForm
from service.models import RecipeService

class ServiceForm(ModelForm):
    class Meta:
        model = RecipeService
        exclude = ("cost_at_serve",)
