from django.db import models
from django.contrib.auth.models import User
from inventory.models import Restaurant

#associates a user to a restaurant
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)

    def __str__(self):
        return self.user.username