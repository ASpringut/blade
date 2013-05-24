import django_tables2 as tables
from django_tables2.utils import A
from service.models import RecipeService

class ServiceTable(tables.Table):
    class Meta:
        model = RecipeService
        attrs = {"class": "table table-stripped"}
        exclude = ('id',)
