from django import forms

class Pump_choose_form(forms.Form):
    choices = [
        ('Gr', 'Grundfos'),
        ('Gr' ,'Grandfoss'), 
        ('Gr','Graubdogs'),
        ('TPY','The_Pumps_Yopta')
    ]
    field_manufact = forms.ChoiceField(choices= choices)