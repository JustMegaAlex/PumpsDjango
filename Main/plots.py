
import numpy as np
from scipy.interpolate import interp1d

# prevent runtime error
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt

def create_plot_image(mark_inst, work_point = None):

    interp_points = 40
    interp_kind = 'quadratic'
    truncate_koef = 1.2
    load_q = None
    load_h = None
    load_eff = None
    load_npsh = None
    load_p2 = None

    q_points_coarse = get_list_points(mark_inst.q_curve_points)
    q_points = np.linspace(q_points_coarse[0], q_points_coarse[-1], interp_points, endpoint = True)

    path1 = '/static/images/pq_and_eff.png'
    path2 = '/static/images/npsh.png'
    path3 = '/static/images/p2.png'
    
    plt.clf() # clean plots

    # interpolate curves
    h_fun = interp1d(q_points_coarse, get_list_points(mark_inst.h_curve_points), kind = interp_kind)
    eff_fun = interp1d(q_points_coarse, get_list_points(mark_inst.efficiency_curve_points), kind = interp_kind)
    npsh_fun = interp1d(q_points_coarse, get_list_points(mark_inst.npsh_curve_points), kind = interp_kind)
    p2_fun = interp1d(q_points_coarse, get_list_points(mark_inst.p2_curve_points), kind = interp_kind)

    # plot H-Q curve
    plt.plot(q_points, h_fun(q_points))

    # plot workpoint and load H-Q curve
    if work_point:
        if work_point[0] > 0 and work_point[1] > 0:
            # plot work_point
            plt.plot(work_point[0], work_point[1], 'ro')

            # compute and plot load curve
            koef = work_point[1]/work_point[0]**2
            h_load_points_coarse = [koef*q**2 for q in q_points_coarse]
            h_load_fun = interp1d(q_points_coarse, h_load_points_coarse, kind = interp_kind)
            load_q, load_h = get_intersect_point(h_fun, h_load_fun, segment = (q_points_coarse[0], q_points_coarse[-1]))
            
            if load_q:
                # compute index to truncate load curve
                i = 0
                while q_points[i] < load_q:
                    i += 1
                i = round(i*truncate_koef)
                # plot curve truncated
                plt.plot(q_points[:i], h_load_fun(q_points[:i]))
                plt.plot(load_q, load_h, 'ro')

                # compute other curves' values
                load_eff = eff_fun(load_q)
                load_npsh = npsh_fun(load_q)
                load_p2 = p2_fun(load_q)

    # plot eff-Q curve
    ax_eff = plt.twinx()
    eff_points = eff_fun(q_points)
    ax_eff.plot(q_points, eff_points)
    # get efficiency max value
    eff_max = max(eff_points)
    # set plot y lim(it
    ax_eff.set_ylim((0, eff_max*3))
    plt.savefig('Main/' + path1)
    
    # plot npsh-Q curve
    plt.clf()
    plt.plot(q_points, npsh_fun(q_points))
    plt.savefig('Main/' + path2)

    # plot p2-Q curve
    plt.clf()
    plt.plot(q_points, p2_fun(q_points))
    plt.savefig('Main/' + path3)

    if load_q != None:
        load_q = formatted(load_q)
        load_h = formatted(load_h)
        load_eff = formatted(load_eff)
        load_p2 = formatted(load_p2)
        load_npsh = formatted(load_npsh)

    curves_data = {
        'img1': path1,
        'img2': path2,
        'img3': path3,
        'load_q': load_q,
        'load_h': load_h,
        'load_eff': load_eff,
        'load_npsh': load_npsh,
        'load_p2': load_p2
    }
    
    return curves_data

def get_list_points(str_curve, old_x = None, new_x = None):
    '''
    converts string of comma-separated floats into a list of floats
    :input: [str]
    :returns: a list of floats
    '''
    return [float(s) for s in str_curve.split(',')]


def get_intersect_point(f1, f2, segment, tol = 0.001, max_iters = 1000):
    max_x = segment[1]
    min_x = segment[0]
    if f1(min_x) < f2(min_x):
        f1, f2 = f2, f1
    x = (max_x - min_x)*0.5
    y1 = f1(x)
    y2 = f2(x)
    diff = y1 - y2

    while (abs(diff) > tol) and max_iters:
        max_iters -= 1
        if diff > 0:
            min_x = x
            x = x + (max_x - x)*0.5
            y1 = f1(x)
            y2 = f2(x)
            diff = y1 - y2
        else:
            max_x = x
            x = x - (x - min_x)*0.5
            y1 = f1(x)
            y2 = f2(x)
            diff = y1 - y2

    if not max_iters and (abs(diff) > tol):
        print('get_intersect_point: intersection point not found')
        return None, None

    return x, y1

def formatted(f):
    return '{:.2f}'.format(f)