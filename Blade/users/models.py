from django.db import models
from django.contrib.auth.models import User
from inventory.models import Resturant

#associates a user to a resturant
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    resturant = models.ForeignKey(Resturant)

    def __str__(self):
        return self.user.username