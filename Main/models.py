from django.db import models
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(max_length = 60, blank = True, default = 'Unnamed')


class Equipment_type(models.Model):
    type = models.CharField(max_length = 30, blank = True, default = 'Unnamed')
    manufacturer = ChainedForeignKey(
        Manufacturer,
        chained_field="manufacturer",
        chained_model_field="manufacturer",
        show_all=False,
        auto_choose=True,
        sort=True
    )