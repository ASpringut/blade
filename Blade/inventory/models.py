from django.db import models
from django.contrib.auth.models import User
from Measures.models import Unit

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
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.ForeignKey(Unit)
    date_modified = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return self.name
    
    def to_tuple(self):
        return (self.name,
                float(self.amount), 
                ''.join([self.unit.name,'s']), 
                self.date_modified.strftime('%d-%m-%y %I:%M %p'))
    
    class Meta:
        ordering = ('name',)

    
            
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
    unit = models.ForeignKey(Unit)

