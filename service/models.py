from django.db import models
from recipes.models import Recipe

# Create your models here.
class RecipeService(models.Model):
    recipe = models.ForeignKey(Recipe)
    number = models.PositiveIntegerField()
    date = models.DateField(auto_now_add = True)
    recipe_cost_at_serve = models.DecimalField(max_digits=6, decimal_places=2)
    cost_at_serve = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return ' '.join([str(self.recipe), str(self.number), str(self.date)])


