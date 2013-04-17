from django.db import models
from inventory.models import Resturant, Ingredient
from Measures.models import Unit

            
class Recipe(models.Model):
    resturant = models.ForeignKey(Resturant)
    name = models.CharField(max_length = 30)
    instruction = models.CharField(max_length = 1024)
    
    def __str__(self):
        return self.name

    def get_ingredients(self):
        ingredients = RecipeIngredient.objects.filter(recipe = self.id)
        return ingredients
    
    class Meta:
        ordering = ('name',)

        
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.ForeignKey(Unit)
    
    def __str__(self):
        return self.recipe.name+' '+str(self.ingredient)+' '+str(self.amount)+self.unit.abbv

