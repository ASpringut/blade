import django_tables2 as tables
from inventory.models import Ingredient

class IngredientTable(tables.Table):
    delete = tables.CheckBoxColumn(accessor="pk", orderable=False)
    class Meta:
        model = Ingredient
        attrs = {"class":"table table-stripped"}
        sequence = ("name","amount","unit","cost_per_unit","date_modified")
        exclude = ("id","restaurant")
        include = ()

