
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt

def create_plot_image(mark_inst, work_point = None):

    interp_points = 40
    interp_kind = 'quadratic'

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
        plt.plot(work_point[0], work_point[1], 'ro')

        if work_point[0] > 0 and work_point[1] > 0:
            koef = work_point[1]/work_point[0]**2
            h_load_points = [koef*q**2 for q in q_points_coarse]
            h_load_fun = interp1d(q_points_coarse, h_load_points, kind = interp_kind)
            plt.plot(q_points, h_load_fun(q_points))

    # plot eff-Q curve
    ax_eff = plt.twinx()
    ax_eff.plot(q_points, eff_fun(q_points))
    plt.savefig('Main/' + path1)
    
    # plot npsh-Q curve
    plt.clf()
    plt.plot(q_points, npsh_fun(q_points))
    plt.savefig('Main/' + path2)

    # plot p2-Q curve
    plt.clf()
    plt.plot(q_points, p2_fun(q_points))
    plt.savefig('Main/' + path3)

    image_paths = {
        'img1':path1,
        'img2':path2,
        'img3':path3
    }
    
    return image_paths

def get_list_points(str_curve, old_x = None, new_x = None):
    '''
    converts string of comma-separated floats into a list of floats
    :input: [str]
    :returns: a list of floats
    '''
    return [float(s) for s in str_curve.split(',')]
