from django.db import models

from Measures.models import Unit

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
        
        
class Ingredient(models.Model):



    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length = 30)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    unit = models.ForeignKey(Unit)
    date_modified = models.DateTimeField(auto_now = True)
    cost_per_unit = models.DecimalField(max_digits = 9, decimal_places=2)

    def __str__(self):
        return self.name
    
    def to_tuple(self):
        return (self.name,
                float(self.amount), 
                ''.join([self.unit.name,'s']),
                float(self.cost_per_unit),
                self.date_modified.strftime('%d-%m-%y %I:%M %p'))
    
    class Meta:
        ordering = ('name',)

    
