import os
import pandas as pd
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import Choose
from .models import Manufacturer, Eq_type, Eq_model, Eq_mark
from .plots import create_plot_image



def pumps(request):

    manuf = request.POST.get('manufacturer')
    eq_type = request.POST.get('eq_type')
    eq_model = request.POST.get('eq_model')
    eq_mark = request.POST.get('eq_mark')
    _x = request.POST.get('x_coord')
    _y = request.POST.get('y_coord')
    work_point = (float(_x), float(_y)) if _x  and _y  else None

    context = {}

    if eq_mark:
        eq_mark_inst = Eq_mark.objects.get(eq_mark = eq_mark)
        curves_data = create_plot_image(eq_mark_inst, work_point = work_point)
        context.update(curves_data)

    form = Choose(ch_manuf = manuf, ch_model = eq_model, ch_type = eq_type, point_x = _x, point_y = _y)
    context['form'] = form
    return render(request, 'main/pumps.html', context)

def update_data(request):

    manufacturer = 'Grundfos'
    eq_model = 'CR'
    eq_type = '1s'
    manuf_inst = Manufacturer.objects.get(name = manufacturer)

    table = pd.read_excel('Data/data.xlsx', sheet_name = manufacturer)
    rows_total = table.count()[0]
    points_count = 6

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
        q_points = [str(table[f'q{point}'][row]) for point in range(points_count)]
        p2_points = [str(table[f'p2{point}'][row]) for point in range(points_count)]
        npsh_points = [str(table[f'npsh{point}'][row]) for point in range(points_count)]
        efficiency_points = [str(table[f'eff{point}'][row]) for point in range(points_count)]
        h_points = [str(table[f'h{point}'][row]) for point in range(points_count)]

        try:
            mark_inst = Eq_mark.objects.get(eq_mark = eq_mark, manufacturer = manuf_inst, eq_type = type_inst)
        except ObjectDoesNotExist:
            mark_inst = Eq_mark(eq_mark = eq_mark, manufacturer = manuf_inst, eq_type = type_inst)
        
        mark_inst.h_curve_points = ','.join(h_points)
        mark_inst.q_curve_points = ','.join(q_points)
        mark_inst.p2_curve_points = ','.join(p2_points)
        mark_inst.npsh_curve_points = ','.join(npsh_points)
        mark_inst.efficiency_curve_points = ','.join(efficiency_points)
        mark_inst.save()

    print('Updated succefully!')
    
    return render(request, 'main/pumps.html')