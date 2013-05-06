from django.db import models
from inventory.models import Restaurant, Ingredient
from Measures.models import Unit

            
class Recipe(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length = 30)
    instruction = models.CharField(max_length = 1024)
    
    def __str__(self):
        return self.name

    def get_ingredients(self):
        ingredients = RecipeIngredient.objects.filter(recipe = self.id)
        return ingredients
    
    def get_cost(self):

        #just sum up the cost of all the ingredients
        ingredients = self.get_ingredients()

        cost = sum([ingredient.get_cost() for ingredient in ingredients])
        return cost


    class Meta:
        ordering = ('name',)

        
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.ForeignKey(Unit)
    
    def __str__(self):
        return self.recipe.name+' '+str(self.ingredient)+' '+str(self.amount)+self.unit.abbv

    def get_cost(self):

        cost = float(self.amount) * self.get_cost_per_unit()

        return cost

    #gets the cost per unit in terms of this recipes unit
    def get_cost_per_unit(self):
        ing_unit = self.ingredient.unit
        recipe_unit = self.unit
        ing_cost = float(self.ingredient.cost_per_unit)

        cost_p_u = ing_cost*recipe_unit.factor/ing_unit.factor

        return cost_p_u

class RecipeService(models.Model):
    recipe = models.ForeignKey(Recipe)
    number = models.PositiveIntegerField()
    date = models.DateField(auto_now_add = True)



