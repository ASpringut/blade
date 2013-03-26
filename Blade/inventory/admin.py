from inventory.models import Resturant, Ingredient, RecipeIngredient, Recipe, UserProfile, IngredientQuantity
from django.contrib import admin

admin.site.register(Resturant)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Recipe)
admin.site.register(UserProfile)
admin.site.register(IngredientQuantity)