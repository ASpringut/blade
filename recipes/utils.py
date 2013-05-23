from recipes.models import Recipe, RecipeIngredient


def delete_recipe(rest, post):
    #get the ids of the recipes to delete
    delete_list = post.getlist("delete_recipe")
    #get the ids of 
    delete_list = [Recipe.objects.get(pk=int(rec_id)) for rec_id in delete_list]
    for rec in delete_list:
        #check if the ingredient belongs to the restaurant of the current user
        if (rec.restaurant == rest):
            #delete the ingredients
            rec.delete()    