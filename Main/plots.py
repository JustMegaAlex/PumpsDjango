
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt

def create_plot_image(mark_inst, work_point = None):

    interpolate_points = 40

    q_points_coarse = get_list_points(mark_inst.q_curve_points)
    q_points = np.linspace(q_points_coarse[0], q_points_coarse[-1], interpolate_points, endpoint = True)

    path1 = '/static/images/pq_and_eff.png'
    path2 = '/static/images/npsh.png'
    path3 = '/static/images/p2.png'
    
    plt.clf() # clean plots

    plt.plot(q_points, get_list_points(mark_inst.h_curve_points, q_points_coarse, q_points))

    # add workpoint
    if work_point:
        plt.plot(work_point[0], work_point[1], 'ro')

    ax_eff = plt.twinx()
    ax_eff.plot(q_points, get_list_points(mark_inst.efficiency_curve_points, q_points_coarse, q_points))
    plt.savefig('Main/' + path1)
    
    plt.clf()
    plt.plot(q_points, get_list_points(mark_inst.npsh_curve_points, q_points_coarse, q_points))
    plt.savefig('Main/' + path2)

    plt.clf()
    plt.plot(q_points, get_list_points(mark_inst.p2_curve_points, q_points_coarse, q_points))
    plt.savefig('Main/' + path3)

    image_paths = {
        'img1':path1,
        'img2':path2,
        'img3':path3
    }
    
    return image_paths

def get_list_points(str_curve, old_x = None, new_x = None):

    y = [float(s) for s in str_curve.split(',')]

    if not old_x:
        return y

    print(old_x, new_x, y)

    interp = interp1d(old_x, y, kind = 'quadratic')

    return interp(new_x)