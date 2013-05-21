import django_tables2 as tables
from models import RecipeService

class ServiceTable(tables.Table):
    class Meta:
        model = RecipeService
        attrs = {"class": "table table-stripped"}