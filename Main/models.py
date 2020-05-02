from django.db import models

# Create your models here

class Manufacturer(models.Model):
    name = models.CharField(max_length = 60, blank = True, default = 'Unnamed')

class Eq_model(models.Model):
    eq_model = models.CharField(max_length = 30, blank = True, default = 'Unnamed')
    manufacturer = models.ForeignKey(Manufacturer, on_delete= models.CASCADE)

class Eq_type(models.Model):
    eq_type = models.CharField(max_length = 30, blank = True, default = 'Unnamed')
    eq_model = models.ForeignKey(Eq_model, on_delete= models.CASCADE)

class Eq_mark(models.Model):
    eq_mark = models.CharField(max_length = 60, blank = True, default = 'Unnamed')
    manufacturer = models.ForeignKey(Manufacturer, on_delete= models.CASCADE)
    eq_type = models.ForeignKey(Eq_type, on_delete= models.CASCADE)

    # curves fields
    default_curve_string = '0.00'*14 + '0.00' + ';' + '0.00'*14 + '0.00'
    pq_curve_points = models.CharField(max_length= 150, blank = True, default = default_curve_string)
    p2_curve_points = models.CharField(max_length= 150, blank = True, default = default_curve_string)
    npsh_curve_points = models.CharField(max_length= 150, blank = True, default = default_curve_string)
    efficency_curve_points = models.CharField(max_length= 150, blank = True, default = default_curve_string)