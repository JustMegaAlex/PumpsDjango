
from django import forms
from .models import Equipment_type

class Pumps_form(forms.Form):
    manufacturer = forms.ChoiceField()

    def __init__(self, **kwargs):
        super(Pumps_form, self).__init__(*args, **kwargs)
        manuf = kwargs['manufacturer']
        self.fields['manufacturer'].choices = Equipment_type.objects.filter(name = manuf)

class Choose_form(forms.ModelForm):

    class Meta:
        model = Equipment_type
        fields = ['manufacturer' ,'type']