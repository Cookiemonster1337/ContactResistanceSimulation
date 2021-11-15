import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
import numpy as np
from timeit import default_timer as timer
from scipy.interpolate import griddata
import plotly.graph_objects as go

def create_gdltopo(res, area, gdl_params):

    # define required gdl-area
    topo_xy = math.sqrt(area)

    # calculate gdl-volume in specified area
    gdl_vol = gdl_params['gdl_thk [µm]']*10**-6 * topo_xy*10**-3 * topo_xy*10**-3

    # calculate total fiber lenght in volume with given gdl-parameters
    tot_fiber_len =  (gdl_vol * (1 - gdl_params['porosity'])) / (0.25 * math.pi * (gdl_params['fiber_dia [µm]']*10**-6)**2)
    # calculate number of fiber layers depending on given thickness of fibers and binderlayers
    layer_num = gdl_params['gdl_thk [µm]'] / (gdl_params['fiber_dia [µm]'] + gdl_params['binder_thk [µm]'])
    # caculate total fiber length in one (contact) layer
    layer_fiber_len = tot_fiber_len / layer_num

    # datapoints of desired model
    digits_xy = int(res*topo_xy+1)

    # initalize arrays of gdl-asperity datapoints (fibers) and asprity-maxima of gdl-fibers (gdl_peaks)
    gdl_fibers = []
    gdl_peaks = []
    # transform fiber_len unit to µm
    fiber_len = int(layer_fiber_len * 1 * 10 ** 6)
    # calc fiber radius
    r = gdl_params['fiber_dia [µm]'] / 2

    # function to generate height distribution of along y-axis on given datapoint
    def fiber_coords_y(datapoint):
        gdl_fibers.append(datapoint)
        gdl_peaks.append(datapoint)
        for i in range(1, int(r)):
            z = round(math.sin(math.acos(i / r)) * r, 2)
            datapoint_up = [datapoint[0], datapoint[1] + i, z]
            gdl_fibers.append(datapoint_up)
            datapoint_down = [datapoint[0], datapoint[1] - i, z]
            gdl_fibers.append(datapoint_down)

    # function to generate height distribution of along x-axis on given datapoint
    def fiber_coords_x(datapoint):
        gdl_fibers.append(datapoint)
        gdl_peaks.append(datapoint)
        for i in range(1, int(r)):
            z = round(math.sin(math.acos(i / r)) * r, 2)
            datapoint_up = [datapoint[0] + i, datapoint[1], z]
            gdl_fibers.append(datapoint_up)
            datapoint_down = [datapoint[0] - i, datapoint[1], z]
            gdl_fibers.append(datapoint_down)

    # function to determine datapoints of fiber in given direction (randomly chosen)
    def fiber_path(p, direction, start, fiber_len):
        gdl_peaks.append(p)
        gdl_fibers.append(p)
        # north
        if direction == 0:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                if start == 3:
                    p = [p[0], p[1] + 1, r]
                elif start == 1:
                    p = [p[0], p[1] - 1, r]
                else:
                    break
                fiber_len += -1
                # fiber_coords_y(p)
                # if p in gdl_peaks:
                #     break
                gdl_fibers.append(p)
                gdl_peaks.append(p)
                for i in range(1, int(r+ 1)):
                    z = round(math.sin(math.acos(i / r)) * r, 2)
                    digit_right = [p[0] + i, p[1], z]
                    digit_left = [p[0] - i, p[1], z]
                    dp_data = [digit_right, digit_left]
                    gdl_fibers.extend(dp_data)
        # north north east
        elif direction == 1:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                if start == 0 or start == 3:
                    p = [p[0] + 1, p[1] + 2, r]
                else:
                    p = [p[0] - 1, p[1] - 2, r]
                fiber_len += -1.7321
                # fiber_coords_y(p)
                # if p in gdl_peaks:
                #     break
                gdl_fibers.append(p)
                gdl_peaks.append(p)
                for i in range(1, int((r+1) / math.sqrt(3))):
                    z = round(math.sin(math.acos((i * math.sqrt(5)) / r)) * r, 2)
                    z2 = round(math.sin(math.acos(((math.sin(22.5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z3 = round(math.sin(math.acos(((math.sin(22.5) * 2 + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z4 = round(math.sin(math.acos((math.sin(67.5) * math.sqrt(2) * i) / r)) * r, 2)
                    z5 = round(math.sin(math.acos(((math.sin(45) * math.sqrt(5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z6 = round(math.sin(math.acos(((math.sin(67.5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z7 = round(math.sin(math.acos(((math.sin(67.5) * 2 + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z8 = round(math.sin(math.acos((math.sin(22.5) * math.sqrt(2) * i) / r)) * r, 2)

                    digit_ull = [p[0] - i * 2, p[1] + i, z]
                    digit_brr = [p[0] + i * 2, p[1] - i, z]

                    digit_u = [p[0] - ((i - 1) * 2), p[1] + (i - 1) + 1, z2]
                    digit_uu = [p[0] - ((i - 1) * 2), p[1] + (i - 1) + 2, z3]
                    digit_ul = [p[0] - ((i - 1) * 2) - 1, p[1] + (i - 1) + 1, z4]
                    digit_uul = [p[0] - ((i - 1) * 2) + 2, p[1] + (i - 1) - 1, z5]

                    digit_r = [p[0] + ((i - 1) * 2) + 1, p[1] - (i - 1), z6]
                    digit_rr = [p[0] + ((i - 1) * 2) + 2, p[1] - (i - 1), z7]
                    digit_ru = [p[0] + ((i - 1) * 2) + 1, p[1] - (i - 1) + 1, z8]
                    digit_rru = [p[0] + ((i - 1) * 2) + 2, p[1] - (i - 1) + 1, z5]

                    dp_data = [digit_ull, digit_brr, digit_u, digit_uu, digit_ul, digit_uul, digit_r, digit_rr,
                               digit_ru, digit_rru]
                    gdl_fibers.extend(dp_data)

        # north east
        elif direction == 2:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                if start == 0 or start == 3:
                    p = [p[0] + 1, p[1] + 1, r]
                else:
                    p = [p[0] - 1, p[1] - 1, r]
                fiber_len += -1.4142
                # fiber_coords_y(p)
                # if p in gdl_peaks:
                #     break
                gdl_fibers.append(p)
                gdl_peaks.append(p)
                for i in range(1, int((r+1) / math.sqrt(2))):
                    z = round(math.sin(math.acos((i * math.sqrt(2)) / r)) * r, 2)
                    z2 = round(math.sin(math.acos((i * math.sin(45)) / r)) * r, 2)
                    digit_ul = [p[0] - i, p[1] + i, z]
                    digit_br = [p[0] + i, p[1] - i, z]
                    digit_u = [p[0] - (i-1), p[1] + (i-1) + 1, z2]
                    digit_r = [p[0] + (i-1) + 1, p[1] - (i-1), z2]
                    dp_data = [digit_ul, digit_br, digit_u, digit_r]
                    gdl_fibers.extend(dp_data)

        # north east east
        elif direction == 3:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                if start == 0 or start == 3:
                    p = [p[0] + 2, p[1] + 1, r]
                else:
                    p = [p[0] - 2, p[1] - 1, r]
                fiber_len += -1.7321
                # fiber_coords_y(p)
                # if p in gdl_peaks:
                #     break
                gdl_fibers.append(p)
                gdl_peaks.append(p)
                for i in range(1, int((r+1) / math.sqrt(3))):
                    z = round(math.sin(math.acos((i * math.sqrt(5)) / r)) * r, 2)
                    z2 = round(math.sin(math.acos(((math.sin(67.5) * 1 + (i-1) * math.sqrt(5)) / r))) * r, 2)
                    z3 = round(math.sin(math.acos(((math.sin(67.5) * 2 + (i-1) * math.sqrt(5)) / r))) * r, 2)
                    z4 = round(math.sin(math.acos(((math.sin(22.5) * math.sqrt(2) + (i-1) * math.sqrt(5)) / r))) * r, 2)
                    z5 = round(math.sin(math.acos(((math.sin(45) * math.sqrt(5) + (i-1) * math.sqrt(5)) / r))) * r, 2)
                    z6 = round(math.sin(math.acos(((math.sin(22.5) * 1 + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z7 = round(math.sin(math.acos(((math.sin(22.5) * 2 + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z8 = round(math.sin(math.acos(((math.sin(67.5) * math.sqrt(2) + (i - 1) * math.sqrt(5)) / r))) * r, 2)

                    digit_uul = [p[0] - i, p[1] + i * 2, z]
                    digit_bbr = [p[0] + i, p[1] - i*2, z]

                    digit_u = [p[0] - (i-1), p[1] + ((i-1)*2) + 1, z2]
                    digit_uu = [p[0] - (i-1), p[1] + ((i-1)*2) + 2, z3]
                    digit_ur = [p[0] - (i-1) + 1, p[1] + ((i-1)*2) + 1, z4]
                    digit_uur = [p[0] - (i-1) + 2, p[1] + ((i-1)*2) + 1, z5]

                    digit_r = [p[0] + (i-1) + 1, p[1] - ((i-1)*2), z6]
                    digit_rr = [p[0] + (i-1) + 2, p[1] - ((i-1)*2), z7]
                    digit_rb = [p[0] + (i-1) + 1, p[1] - ((i-1)*2) - 1, z8]
                    digit_rrb = [p[0] + (i-1) + 2, p[1] - ((i-1)*2) - 1, z5]

                    dp_data = [digit_uul, digit_bbr, digit_u, digit_uu, digit_ur, digit_uur, digit_r, digit_rr,
                               digit_rb, digit_rrb]
                    gdl_fibers.extend(dp_data)

        # east
        elif direction == 4:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                if start == 0:
                    p = [p[0] + 1, p[1] + 0, r]
                elif start == 2:
                    p = [p[0] - 1, p[1] + 0, r]
                else:
                    break
                fiber_len += -1
                #fiber_coords_y(p)
                # if p in gdl_peaks:
                #     break
                gdl_fibers.append(p)
                gdl_peaks.append(p)
                for i in range(1, int(r + 1)):
                    z = round(math.sin(math.acos(i / r)) * r, 2)
                    digit_top = [p[0], p[1] + i, z]
                    digit_bot = [p[0], p[1] - i, z]
                    dp_data = [digit_top, digit_bot]
                    gdl_fibers.extend(dp_data)

        # south east east
        elif direction == 5:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                if start == 0 or start == 1:
                    p = [p[0] + 2, p[1] - 1, r]
                else:
                    p = [p[0] - 2, p[1] + 1, r]
                fiber_len += -1.7321
                # fiber_coords_y(p)
                # if p in gdl_peaks:
                #     break
                gdl_fibers.append(p)
                gdl_peaks.append(p)
                for i in range(1, int((r+1) / math.sqrt(3))):
                    z = round(math.sin(math.acos((i * math.sqrt(5)) / r)) * r, 2)
                    z2 = round(math.sin(math.acos(((math.sin(22.5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z3 = round(math.sin(math.acos(((math.sin(22.5) * 2 + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z4 = round(math.sin(math.acos((math.sin(67.5) * math.sqrt(2) + (i - 1) * math.sqrt(5)) / r)) * r, 2)
                    z5 = round(math.sin(math.acos(((math.sin(45) * math.sqrt(5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z6 = round(math.sin(math.acos(((math.sin(67.5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z7 = round(math.sin(math.acos(((math.sin(67.5) * 2 + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z8 = round(math.sin(math.acos((math.sin(22.5) * math.sqrt(2) + (i - 1) * math.sqrt(5)) / r)) * r, 2)
                    z9 = round(math.sin(math.acos(((math.sin(45) * math.sqrt(5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)

                    digit_uur = [p[0] + i, p[1] + i*2, z]
                    digit_bbl = [p[0] - i, p[1] - i * 2, z]

                    digit_r = [p[0] + (i - 1) + 1, p[1] + ((i - 1) * 2), z2]
                    digit_rr = [p[0] + (i - 1) + 2, p[1] + ((i - 1) * 2), z3]

                    digit_ur = [p[0] + (i - 1) + 1, p[1] + ((i - 1) * 2) + 1, z4]
                    digit_urr = [p[0] + (i - 1) + 2, p[1] + ((i - 1) * 2) + 1, z5]

                    digit_b = [p[0] - (i - 1), p[1] - ((i - 1) * 2) - 1, z6]
                    digit_bb = [p[0] - (i - 1), p[1] - ((i - 1) * 2) - 2, z7]

                    digit_br = [p[0] - (i - 1) + 1, p[1] - ((i - 1) * 2) - 1, z8]
                    digit_bbr = [p[0] - (i - 1) + 1, p[1] - ((i - 1) * 2) - 2, z9]


                    dp_data = [digit_uur, digit_bbl, digit_r, digit_rr, digit_ur, digit_urr, digit_b, digit_bb,
                               digit_br, digit_bbr]
                    gdl_fibers.extend(dp_data)

        # south east
        elif direction == 6:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                if start == 0 or start == 1:
                    p = [p[0] + 1, p[1] - 1, r]
                else:
                    p = [p[0] - 1, p[1] + 1, r]
                fiber_len += -1.4142
                # fiber_coords_y(p)
                # if p in gdl_peaks:
                #     break
                gdl_fibers.append(p)
                gdl_peaks.append(p)
                for i in range(1, int((r+1)/math.sqrt(2))):
                    z = round(math.sin(math.acos((i * math.sqrt(2)) / r)) * r, 2)
                    z2 = round(math.sin(math.acos((i * math.sin(45)) / r)) * r, 2)

                    digit_ur = [p[0] + i, p[1] + i, z]
                    digit_bl = [p[0] - i, p[1] - i, z]

                    digit_r = [p[0] + (i-1) + 1, p[1] + (i-1), z2]
                    digit_b = [p[0] - (i-1), p[1] - (i-1) - 1, z2]

                    dp_data = [digit_ur, digit_bl, digit_r, digit_b]
                    gdl_fibers.extend(dp_data)

        # south south east
        elif direction == 7:
            while p[0] in range(digits_xy) and p[1] in range(digits_xy) and fiber_len > 0:
                if start == 0 or start == 1:
                    p = [p[0] + 1, p[1] - 2, r]
                else:
                    p = [p[0] - 1, p[1] + 2, r]
                fiber_len += -1.7321
                # fiber_coords_y(p)
                # if p in gdl_peaks:
                #     break
                gdl_fibers.append(p)
                gdl_peaks.append(p)
                for i in range(1, int((r+1)/math.sqrt(3))):
                    z = round(math.sin(math.acos((i * math.sqrt(5)) / r)) * r, 2)
                    z2 = round(math.sin(math.acos(((math.sin(67.5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z3 = round(math.sin(math.acos(((math.sin(67.5) * 2 + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z4 = round(math.sin(math.acos((math.sin(22.5) * math.sqrt(2) + (i - 1) * math.sqrt(5)) / r)) * r, 2)
                    z5 = round(math.sin(math.acos(((math.sin(67.5) * math.sqrt(5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z6 = round(math.sin(math.acos(((math.sin(22.5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z7 = round(math.sin(math.acos(((math.sin(22.5) * 2 + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z8 = round(math.sin(math.acos(((math.sin(67.5) * math.sqrt(2) + (i - 1) * math.sqrt(5)) / r))) * r, 2)
                    z9 = round(math.sin(math.acos(((math.sin(45) * math.sqrt(5) + (i - 1) * math.sqrt(5)) / r))) * r, 2)

                    digit_urr = [p[0] + i*2, p[1] + i, z]
                    digit_bll = [p[0] - i*2, p[1] - i, z]

                    digit_r = [p[0] + ((i - 1) * 2) + 1, p[1] + (i - 1), z2]
                    digit_rr = [p[0] + ((i - 1) * 2) + 2, p[1] + (i - 1), z3]

                    digit_br = [p[0] + ((i - 1) * 2) + 1, p[1] + (i - 1) - 1, z4]
                    digit_brr = [p[0] + ((i - 1) * 2) + 2, p[1] + (i - 1) - 1, z5]

                    digit_b = [p[0] - ((i - 1) * 2), p[1] - (i - 1) - 1, z6]
                    digit_bb = [p[0] - ((i - 1) * 2), p[1] - (i - 1) - 2, z7]

                    digit_bl = [p[0] - ((i - 1) * 2), p[1] - (i - 1) - 1, z8]
                    digit_bbl = [p[0] - ((i - 1) * 2) - 1, p[1] - (i - 1) - 2, z9]

                    dp_data = [digit_urr, digit_bll, digit_r, digit_rr, digit_br, digit_brr, digit_b, digit_bb,
                               digit_bl, digit_bbl]
                    gdl_fibers.extend(dp_data)

        return fiber_len


    while fiber_len > 0:
        # p = [random.randint(1, digits_xy), random.randint(1, digits_xy), r]
        # #fiber_coords_y(p)
        # direction = random.randint(0, 8)
        # fiber_len = fiber_path(p, direction, fiber_len)
        start = random.randint(0, 4)
        if start == 0:
            p = [0, random.randint(1, digits_xy), r]
            # fiber_coords_y(p)
            direction = random.randint(0, 8)
            fiber_len = fiber_path(p, direction, start, fiber_len)
        elif start == 1:
            p = [random.randint(1, digits_xy), digits_xy, r]
            # fiber_coords_x(p)
            direction = random.randint(0, 8)
            fiber_len = fiber_path(p, direction, start, fiber_len)
        elif start == 2:
            p = [digits_xy, random.randint(1, digits_xy), r]
            # fiber_coords_y(p)
            direction = random.randint(0, 8)
            fiber_len = fiber_path(p, direction, start, fiber_len)
        elif start == 3:
            p = [random.randint(1, digits_xy), 0, r]
            # fiber_coords_x(p)
            direction = random.randint(0, 8)
            fiber_len = fiber_path(p, direction, start, fiber_len)

    gdl_coords_xy = [i[:2] for i in gdl_fibers]

    mesh = []
    progress = 1
    for x in range(digits_xy):
        for y in range(digits_xy):
            if [x, y] not in gdl_coords_xy:
                mesh.append([x, y, 0])
            progress += 1

    gdltopo = mesh + gdl_fibers

    return gdltopo, gdl_peaks, gdl_fibers

def gdltopo_3d(res, gdltopo, zlim):
    start = timer()
    print('start generating z-array for plot...')
    X_3d = []
    Y_3d = []
    Z_3d = []

    for data in gdltopo:
        X_3d.append(data[0])
        Y_3d.append(data[1])
        Z_3d.append(data[2])

    end = timer()
    print('z-array generated!' + '(' + str(round(end - start, 2)) + 's)')

    # print('plot matplotlib...')
    # start = timer()
    #
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # trisurf = ax.plot_trisurf(X_3d, Y_3d, Z_3d, cmap=cm.jet, linewidth=0.1, antialiased=True)
    #
    # fig.colorbar(trisurf, ax=ax, shrink=0.3, aspect=10, pad=0.15)
    # ax.set_title('Surface Topology - GDL')
    #
    # # Adding labels
    # ax.set_xlabel('µm')
    # ax.set_ylabel('µm')
    # ax.set_zlabel('µm')
    #
    # ax.set_zlim(0, zlim)
    #
    # end = timer()
    # print('matplotlib plotted!' + '(' + str(round(end - start, 2)) + 's)')
    #
    # plt.show()

    print('plot plotly...')
    start = timer()
    xi = np.linspace(1, 100, 100)
    yi = np.linspace(1, 100, 100)

    X, Y = np.meshgrid(xi, yi)

    Z = griddata((X_3d, Y_3d), Z_3d, (X, Y), method='nearest')

    plt.pcolormesh(X, Y, Z)
    plt.show()

    fig = go.Figure(data=[go.Surface(z=Z)])

    fig.update_layout(title='Surface Topology - GDL', scene=dict(xaxis_title='x [µm]', yaxis_title=' y [µm]', zaxis_title='z [µm]',
                                                  zaxis=dict(nticks=4, range=[0, 50])))
    end = timer()
    print('plotly plotted!' + '(' + str(round(end - start, 2)) + 's)')
    fig.show()

def gdltopo_2d(gdl):

    X_2d_fiber = []
    Y_2d_fiber = []

    for data in gdl:
        X_2d_fiber.append(data[0])
        Y_2d_fiber.append(data[1])

    plt.scatter(X_2d_fiber, Y_2d_fiber, 0.1)

    plt.title("fiber - coordinates")
    plt.xlabel("µm")
    plt.ylabel("µm")

    plt.show()

def gdlpeaks_2d(gdl_peaks):

    X_2d_center = []
    Y_2d_center = []

    for data in gdl_peaks:
        X_2d_center.append(data[0])
        Y_2d_center.append(data[1])

    plt.scatter(X_2d_center, Y_2d_center, 0.1)

    plt.title("fiber(center) - coordinates")
    plt.xlabel("µm")
    plt.ylabel("µm")

    plt.show()

def gdl_crosssection_2d(gdl, xpos):
    crosssection = []
    Y_2d = []
    Z_2d = []

    for data in gdl:
        if data[0] == xpos:
            crosssection.append([data[1], data[2]])

    print(crosssection)
    crosssection.sort()
    print(crosssection)

    for data in crosssection:
        Y_2d.append(data[0])
        Z_2d.append(data[1])

    plt.ylim(0, 20)
    plt.plot(Y_2d, Z_2d, 0.1)


    plt.title("cross section @xpos: " + str(xpos) + 'µm')
    plt.xlabel("µm")
    plt.ylabel("µm")

    plt.show()