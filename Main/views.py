from django.shortcuts import render
from .forms import Pump_choose_form

# Create your views here.

def pumps_view(request):
    form = Pump_choose_form()
    image_path = None
    if True:
        image_path = '/static/images/fig.png'
    return render(request,'main/main_page.html', {'form': form, 'image_path':image_path})