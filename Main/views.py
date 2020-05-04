import os
import pandas as pd
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from matplotlib import pyplot as plt
from .forms import Choose
from .models import Manufacturer, Eq_type, Eq_model, Eq_mark

def create_plot_image(mark_inst):

    q_points = get_list_points(mark_inst.q_curve_points)
    path1 = '/static/images/pq_and_eff.png'
    path2 = '/static/images/npsh.png'
    path3 = '/static/images/p2.png'
    
    plt.clf() # clean plot
    ax_h = plt.subplot()
    ax_h.plot(q_points, get_list_points(mark_inst.h_curve_points))
    ax_h.spines['left'].set_position(('axes', 0))

    ax_eff = ax_h.twinx()
    ax_eff.plot(q_points, get_list_points(mark_inst.efficiency_curve_points))
    ax_eff.spines['left'].set_position(('axes', 1))
    plt.savefig('Main/' + path1)
    
    plt.clf()
    ax_npsh = ax_h.twinx()
    ax_npsh.plot(q_points, get_list_points(mark_inst.npsh_curve_points))
    plt.savefig('Main/' + path2)

    plt.clf()
    ax_p2 = ax_h.twinx()
    ax_p2.plot(q_points, get_list_points(mark_inst.p2_curve_points))
    plt.savefig('Main/' + path3)

    image_paths = {
        'img1':path1,
        'img2':path2,
        'img3':path3
    }
    
    return image_paths

def get_list_points(str_curve):

    return [float(s) for s in str_curve.split(',')]

def pumps(request):

    manuf = request.POST.get('manuf')
    eq_type = request.POST.get('eq_type')
    eq_model = request.POST.get('eq_model')
    eq_mark = request.POST.get('eq_mark')

    context = {}

    if eq_mark:
        eq_mark_inst = Eq_mark.objects.get(eq_mark = eq_mark)
        image_paths = create_plot_image(eq_mark_inst)
        context.update(image_paths)

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