from django.shortcuts import render
from .forms import Choose_form

def pumps(request):
    form = Choose_form()
    print(type(form))
    return render(request, 'main/pumps.html', {'form':form})

def pumps_slow(request):
    