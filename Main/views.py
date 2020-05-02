import os
import pandas as pd
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from matplotlib import pyplot as plt
from .forms import Choose
from .models import Manufacturer, Eq_type, Eq_model, Eq_mark

def save_plot_as_png(curve_str):
    plt.clf() # clean plot
    y = curve_str.split(';') # x and y points strings
    x = [float(point) for point in y[1].split(',')]
    y = [float(point) for point in y[0].split(',')]
    plt.plot(x, y)
    path = '/static/images/pq.png'
    plt.savefig('Main/static/images/pq.png', )
    return path


def pumps(request):

    manuf = request.POST.get('manuf')
    eq_type = request.POST.get('eq_type')
    eq_model = request.POST.get('eq_model')
    eq_mark = request.POST.get('eq_mark')

    context = {}

    if eq_mark:
        curve_str = Eq_mark.objects.get(eq_mark = eq_mark).pq_curve_points
        plot_img_path = save_plot_as_png(curve_str)
        context['image_path'] = plot_img_path

    print({'manuf':manuf,'eq_model':eq_model, 'eq_type':eq_type})

    form = Choose(ch_manuf = manuf, ch_model = eq_model, ch_type = eq_type)
    context['form'] = form
    return render(request, 'main/pumps.html', context)

def update_data(request):

    manufacturer = 'Grundfos'
    eq_model = 'CR'
    eq_type = '1s'
    manuf_inst = Manufacturer.objects.get(name = manufacturer)

    table = pd.read_excel('Data/data.xlsx', sheet_name = manufacturer)
    rows_total = table.count()[0]

    try:
        model_inst = Eq_model.objects.get(manufacturer = manuf_inst, eq_model = eq_model)
    except ObjectDoesNotExist:
        model_inst = Eq_model(manufacturer = manuf_inst, eq_model = eq_model)
        model_inst.save()
    
    try:
        type_inst = Eq_type.objects.get(eq_model = model_inst, eq_type = eq_type)
    except ObjectDoesNotExist:
        type_inst = Eq_type(eq_model = model_inst, eq_type = eq_type)
        type_inst.save()



    for row in range(rows_total):
        eq_mark = table['mark'][row]
        q_points = [str(table[f'q{point}'][row]) for point in range(points)]
        p2_points = [str(table[f'p2{point}'][row]) for point in range(points)]
        npsh_points = [str(table[f'npsh{point}'][row]) for point in range(points)]
        efficiency_points = [str(table[f'eff{point}'][row]) for point in range(points)]
        h_points = [str(table[f'h{point}'][row]) for point in range(points)]

        h_curve_points = ','.join(q_points)
        q_curve_points = ','.join(q_points)
        p2_curve_points = ','.join(q_points)
        npsh_curve_points = ','.join(q_points)
        efficiency_curve_points = ','.join(q_points)

        try:
            mark_inst = Eq_mark.objects.get(eq_mark = eq_mark, manufacturer = manuf_inst, eq_type = type_inst)
        except ObjectDoesNotExist:
            mark_inst = Eq_mark(eq_mark = eq_mark, manufacturer = manuf_inst, eq_type = type_inst)
        
        mark_inst.pq_curve_points = curve_str
        mark_inst.save()
    
    return render(request, 'main/pumps.html')