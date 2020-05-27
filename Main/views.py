import os
import pandas as pd
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import Choose, Work_point
from .models import Manufacturer, Eq_type, Eq_model, Eq_mark
from .plots import create_plot_image, get_interp_fun



def pumps(request):

    manuf = request.POST.get('manufacturer')
    eq_type = request.POST.get('eq_type')
    eq_model = request.POST.get('eq_model')
    eq_mark = request.POST.get('eq_mark')
    _x = request.POST.get('x_coord')
    _y = request.POST.get('y_coord')
    work_point = (float(_x), float(_y)) if _x  and _y  else None

    if request.method == 'GET':
        eq_mark = request.GET.get('eq_mark')

    context = {}

    if eq_mark:
        eq_mark_inst = Eq_mark.objects.get(eq_mark = eq_mark)
        curves_data = create_plot_image(eq_mark_inst, work_point = work_point)
        context.update(curves_data)

    form = Choose(ch_manuf = manuf, ch_model = eq_model, ch_type = eq_type, point_x = _x, point_y = _y)
    context['form'] = form
    return render(request, 'main/pumps.html', context)

def choice(request):

    eq_type = '1s'

    eq_type_instance = Eq_type.objects.get(eq_type = eq_type)

    all_marks = Eq_mark.objects.filter(eq_type = eq_type_instance)

    print(all_marks)

    _x = request.POST.get('x_coord')
    _y = request.POST.get('y_coord')
    work_point = (float(_x), float(_y)) if _x  and _y  else None

    context = {}
    context['form'] = Work_point()

    if work_point:

        _x = float(_x)
        _y = float(_y)

        choosed_marks = []

        # choose siutable marks
        for mark in all_marks:

            h_fun = get_interp_fun(mark, 'h')

            compute_y = h_fun(_x)

            delta = _y/compute_y

            if 0.5 < delta < 1.02:

                choosed_marks.append(mark)

        context['marks_list'] = choosed_marks

    return render(request, 'main/choice.html', context)

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