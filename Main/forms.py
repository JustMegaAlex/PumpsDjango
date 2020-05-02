
from django import forms
from .models import Eq_type, Manufacturer, Eq_model, Eq_mark

class Choose(forms.Form):

    choices = [(obj.name, obj.name) for obj in Manufacturer.objects.all()]

    manuf = forms.ChoiceField(required= True, choices = choices)
    eq_model = forms.ChoiceField(required= False)
    eq_type = forms.ChoiceField(required= False)
    eq_mark = forms.ChoiceField(required= False)
    

    def __init__(self, ch_manuf=None, ch_type=None, ch_model = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if ch_type:
            # manuf_obj = Manufacturer.objects.get(name = ch_manuf)
            type_obj = Eq_type.objects.get(eq_type = ch_type)
            # self.initial['eq_type'] = ch_type
            self.fields['eq_mark'].choices = [(obj.eq_mark, obj.eq_mark) for obj in Eq_mark.objects.filter(eq_type = type_obj)]#  Eq_model.objects.filter(manufacturer=manuf_obj, type = type_obj)]
        elif ch_model:
            model_obj = Eq_model.objects.get(eq_model = ch_model)
            self.fields['eq_type'].choices = [(obj.eq_type, obj.eq_type) for obj in Eq_type.objects.filter(eq_model = model_obj)]
        elif ch_manuf:
            manuf_obj = Manufacturer.objects.get(name = ch_manuf)
            self.fields['eq_model'].choices = [(obj.eq_model, obj.eq_model) for obj in Eq_model.objects.filter(manufacturer=manuf_obj)]