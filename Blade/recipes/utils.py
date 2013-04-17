from recipes.models import RecipeIngredient

def ing_formset_inital(recipe):

    #get the relevant ingredients
    print(recipe.get_ingredients())