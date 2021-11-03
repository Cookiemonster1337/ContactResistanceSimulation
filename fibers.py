import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
import numpy as np

def create_gdltopo(res, area, gdl_params):

    topo_xy = math.sqrt(area)
    gdl_vol = gdl_params['gdl_thk [µm]']*10**-6 * topo_xy*10**-3 * topo_xy*10**-3
    #print('gdl vol.:' + gdl_vol)

    tot_fiber_len =  (gdl_vol * (1 - gdl_params['porosity'])) / (0.25 * math.pi * (gdl_params['fiber_dia [µm]']*10**-6)**2)
    #print('tot. fiber length: ' + tot_fiber_len)
    layer_num = gdl_params['gdl_thk [µm]'] / (gdl_params['fiber_dia [µm]'] + gdl_params['binder_thk [µm]'])
    #print('layers#' + layer_num)
    layer_fiber_len = tot_fiber_len / layer_num
    print(layer_fiber_len)

    digits_xy = int(res*topo_xy+1)

    mesh = [[x, y, 0] for x in range(0, digits_xy) for y in range(0, digits_xy)]

    gdl_coords = []
    gdl_peaks = []
    fiber_len = int(layer_fiber_len * 1 * 10 ** 6)
    r = gdl_params['fiber_dia [µm]'] / 2

    def fiber_coords_y(datapoint):
        gdl_coords.append(datapoint)
        gdl_peaks.append(datapoint)
        for i in range(1, int(r) + 1):
            z = round(math.sin(math.acos(i / r)) * r, 2)
            datapoint_up = [datapoint[0], datapoint[1] + i, z]
            gdl_coords.append(datapoint_up)
            datapoint_down = [datapoint[0], datapoint[1] - i, z]
            gdl_coords.append(datapoint_down)


    def fiber_coords_x(datapoint):
        gdl_coords.append(datapoint)
        gdl_peaks.append(datapoint)
        for i in range(1, int(r) + 1):
            z = round(math.sin(math.acos(i / r)) * r, 2)
            datapoint_up = [datapoint[0] + i, datapoint[1], z]
            gdl_coords.append(datapoint_up)
            datapoint_down = [datapoint[0] - i, datapoint[1], z]
            gdl_coords.append(datapoint_down)


    def fiber_path(p, direction, fiber_len):
        if direction == 0:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                p = [p[0] + 1, p[1] + 0, r]
                fiber_len += -1
                fiber_coords_y(p)
        elif direction == 1:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                p = [p[0] + 1, p[1] + 1, r]
                fiber_len += -1.4142
                fiber_coords_y(p)
        elif direction == 2:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                p = [p[0] + 1, p[1] - 1, r]
                fiber_len += -1.4142
                fiber_coords_y(p)
        elif direction == 3:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                p = [p[0] + 1, p[1] + 2, r]
                fiber_len += -1.7321
                fiber_coords_y(p)
        elif direction == 4:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                p = [p[0] + 1, p[1] - 2, r]
                fiber_len += -1.7321
                fiber_coords_y(p)
        elif direction == 5:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                p = [p[0] + 2, p[1] - 1, r]
                fiber_len += -1.7321
                fiber_coords_y(p)
        elif direction == 6:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                p = [p[0] - 2, p[1] - 1, r]
                fiber_len += -1.7321
                fiber_coords_y(p)
        return fiber_len

    while fiber_len > 0:
        start = random.randint(0, 4)
        if start == 0:
            p = [0, random.randint(1, digits_xy), r]
            fiber_coords_y(p)
            direction = random.randint(0, 7)
            fiber_len = fiber_path(p, direction, fiber_len)
        elif start == 1:
            p = [random.randint(1, digits_xy), digits_xy, r]
            fiber_coords_x(p)
            direction = random.randint(0, 3)
            fiber_len = fiber_path(p, direction, fiber_len)
        elif start == 2:
            p = [digits_xy, random.randint(1, digits_xy), r]
            fiber_coords_y(p)
            direction = random.randint(0, 3)
            fiber_len = fiber_path(p, direction, fiber_len)
        elif start == 3:
            p = [random.randint(1, digits_xy), 0, r]
            fiber_coords_x(p)
            direction = random.randint(0, 3)
            fiber_len = fiber_path(p, direction, fiber_len)

    gdl_coords_xy = [i[:2] for i in gdl_coords]
    print(len(gdl_coords_xy))

    mesh = []
    progress = 1
    for x in range(digits_xy):
        for y in range(digits_xy):
            if [x, y] not in gdl_coords_xy:
                mesh.append([x, y, 0])
            progress += 1
        print(str(round((progress / res ** 2) * 100, 0)) + '%')

    gdltopo = mesh + gdl_coords
    return gdltopo, gdl_peaks

def gdltopo_3d(gdltopo):
    X_3d = []
    Y_3d = []
    Z_3d = []

    for data in gdltopo:
        X_3d.append(data[0])
        Y_3d.append(data[1])
        Z_3d.append(data[2])

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    trisurf = ax.plot_trisurf(X_3d, Y_3d, Z_3d, cmap=cm.jet, linewidth=0.1, antialiased=True)

    fig.colorbar(trisurf, ax=ax, shrink=0.3, aspect=10, pad=0.15)
    ax.set_title('Surface Topology - GDL')

    # Adding labels
    ax.set_xlabel('µm')
    ax.set_ylabel('µm')
    ax.set_zlabel('µm')

    ax.set_zlim(0, 50)

    plt.show()
