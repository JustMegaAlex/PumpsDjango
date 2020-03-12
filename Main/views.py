from django.shortcuts import render
from .forms import Pump_choose_form

# Create your views here.

def pumps_view(request):
    form = Pump_choose_form()
    print(form.choices)
    return render(request,'main/main_page.html', {'form': form})