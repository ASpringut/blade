from django.db import models
from django.contrib.auth.models import User


class Resturant(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
        
#associates a user to a resturant
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    resturant = models.ForeignKey(Resturant)

        
class Ingredient(models.Model):


    resturant = models.ForeignKey(Resturant)
    name = models.CharField(max_length = 30)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

                
class IngredientQuantity(models.Model):

    GRAM = 'Gram'
    KILOGRAM = 'Kilogram'
    POUND = 'Pound'

    
    ingredient = models.ForeignKey(Ingredient)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length = 10)
    date_modified = models.DateTimeField(auto_now_add = True)

    
    
    def to_tuple(self):
        return (float(self.amount), 
                ''.join([self.unit,'s']), 
                self.date_modified.strftime('%d-%m-%y %I:%M %p'))
                
    def __unicode__(self):
        return str(self.amount)+" "+self.unit
    
    
            
class Recipe(models.Model):
    resturant = models.ForeignKey(Resturant)
    name = models.CharField(max_length = 30)
    instruction = models.CharField(max_length = 1024)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

        
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length = 10)

