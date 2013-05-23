from recipes.models import RecipeIngredient, Recipe, RecipeService
from django.contrib import admin

admin.site.register(RecipeIngredient)
admin.site.register(Recipe)
admin.site.register(RecipeService)