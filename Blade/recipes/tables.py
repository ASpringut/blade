import django_tables2 as tables
from django_tables2.utils import A
from models import RecipeService, Recipe

class ServiceTable(tables.Table):
    class Meta:
        model = RecipeService
        attrs = {"class": "table table-stripped"}
        exclude = ('id',)

class RecipeTable(tables.Table):
    delete = tables.CheckBoxColumn(accessor="pk", orderable=False)
    #custom column with template for link because linkcolumn does not work
    name_link ='<a href = "../view_recipe?recipe={{record.pk}}">{{record.name}}</a>'
    recipe_name = tables.TemplateColumn(name_link, order_by=A("name"))
    class Meta:
        model = Recipe
        attrs = {"class": "table table-stripped"}
        exclude = ("id", "restaurant", 'name')
        sequence = ("recipe_name",)