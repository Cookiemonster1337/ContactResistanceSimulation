import random
import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

def create_surfacetopo(res, area, topo_params):

    topo_xy = math.sqrt(area)
    digits_xy = int(res * topo_xy + 1)

    print('topo_xy: ' + str(topo_xy))
    print('digits_xy: ' + str(digits_xy))
    mesh = [[x, y] for x in range(digits_xy) for y in range(digits_xy)]

    peak_square = []
    peaks = []
    peak_count = int((topo_params['d_peak'] * topo_xy) ** 2)

    for i in range(peak_count + 1):
        #print(str(round(i / (peak_count + 1) * 100, 2)) + ' %')
        peak = random.choice(mesh)
        peaks.append(peak)
        peak_xrange = range(peak[0] - int(topo_params['r1']), peak[0] + int(topo_params['r1'] + 1))
        peak_yrange = range(peak[1] - int(topo_params['r1']), peak[1] + int(topo_params['r1'] + 1))
        peak_square = [[x, y] for x in peak_xrange for y in peak_yrange]
        mesh = [xy for xy in mesh if xy not in peak_square]
        peak_square.clear()

    bp_coords = []  # 3D-coordinates for peaks
    progress = 0

    for peak in peaks:
        progress += 1
        #print(str(round(progress / (len(peaks)) * 100, 2)) + ' %')
        h = round(random.uniform(topo_params['r1'] - (topo_params['sigma_s'] / 2), topo_params['r1'] +
                                 (topo_params['sigma_s'] / 2)), 2)  # height of peak in given simga_s
        bp_coords.append([peak[0], peak[1], h])
        for i in range(1, int(h + 1)):  # spherical shape
            z = round(math.sin(math.acos(i / h)) * h, 2)
            coords = [[peak[0] - i, peak[1], z], [peak[0] + i, peak[1], z], [peak[0], peak[1] - i, z],
                      [peak[0], peak[1] + i, z],
                      [peak[0] + 1, peak[1] + i, z], [peak[0] + i, peak[1] - i, z], [peak[0] - i, peak[1] + i, z],
                      [peak[0] - i, peak[1] - i, z]]
            if i > 1:
                for a in range(1, i):
                    coords += [[peak[0] + i, peak[1] + a, z], [peak[0] + i, peak[1] - a, z],
                               [peak[0] - i, peak[1] + a, z], [peak[0] - i, peak[1] - a, z],
                               [peak[0] + a, peak[1] + i, z], [peak[0] - a, peak[1] + i, z],
                               [peak[0] + a, peak[1] - i, z], [peak[0] - a, peak[1] - i, z]]
            for coord in coords:
                bp_coords.append(coord)

    bp_coords_xy = [i[:2] for i in bp_coords]

    bp_topo = []
    progress = 1
    for x in range(digits_xy):
        for y in range(digits_xy):
            if [x, y] not in bp_coords_xy:
                bp_topo.append([x, y, 0])
            progress += 1
        #print(str(round((progress / res ** 2) * 100, 0)) + '%')

    bp_topo = bp_topo + bp_coords

    #print(bp_topo)
    return bp_topo, peaks

def surfacetopo_3d(surfacetopo):
    X_3d = []
    Y_3d = []
    Z_3d = []

    for data in surfacetopo:
        X_3d.append(data[0])
        Y_3d.append(data[1])
        Z_3d.append(data[2])

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    trisurf = ax.plot_trisurf(X_3d, Y_3d, Z_3d, cmap=cm.jet, linewidth=0.1, antialiased=True)

    fig.colorbar(trisurf, ax=ax, shrink=0.3, aspect=10, pad=0.15)
    ax.set_title('Surface Topology - BP')

    # Adding labels
    ax.set_xlabel('µm')
    ax.set_ylabel('µm')
    ax.set_zlabel('µm')

    ax.set_zlim(0, 50)

    plt.show()

# d_peak = 200 #peaks/mm
# r1 = 2
# sigma_s = 5
#
# area = 1 #mm2
# bp_x = 0.2 #mm
# bp_y = 0.2 #mm
#
# res = 1000 #mm/µm
#
#
#
# mesh = [[x, y] for x in range(0, int(res*bp_x+1)) for y in range(0, int(res*bp_y+1))]
#
# peak_square = []
# peaks = []
# peak_count = int((d_peak*bp_x)**2)
#
# for i in range(peak_count+1):
#     print(str(round(i / (peak_count+1) * 100, 2)) + ' %')
#     peak = random.choice(mesh)
#     peaks.append(peak)
#     peak_xrange = range(peak[0] - int(r1), peak[0] + int(r1+1))
#     peak_yrange = range(peak[1] - int(r1), peak[1] + int(r1+1))
#     peak_square = [[x, y] for x in peak_xrange for y in peak_yrange]
#     mesh = [xy for xy in mesh if xy not in peak_square]
#     peak_square.clear()
#
# bp_coords = [] # 3D-coordinates for peaks
# progress = 0
#
# for peak in peaks:
#     progress += 1
#     print(str(round(progress/(len(peaks))*100, 2)) + ' %')
#     h = round(random.uniform(r1-(sigma_s/2), r1 + (sigma_s/2)), 2) #height of peak in given simga_s
#     bp_coords.append([peak[0], peak[1], h])
#     for i in range(1, int(h+1)): #spherical shape
#         z = round(math.sin(math.acos(i/h)) * h, 2)
#         coords = [[peak[0]-i, peak[1], z], [peak[0]+i, peak[1], z], [peak[0], peak[1]-i, z], [peak[0], peak[1]+i, z],
#                   [peak[0]+1, peak[1]+i, z], [peak[0]+i, peak[1]-i, z], [peak[0]-i, peak[1]+i, z], [peak[0]-i, peak[1]-i, z]]
#         if i > 1:
#             for a in range(1, i):
#                 coords += [[peak[0]+i, peak[1]+a, z], [peak[0]+i, peak[1]-a, z], [peak[0]-i, peak[1]+a, z], [peak[0]-i, peak[1]-a, z],
#                 [peak[0]+a, peak[1]+i, z], [peak[0]-a, peak[1]+i, z], [peak[0]+a, peak[1]-i, z], [peak[0]-a, peak[1]-i, z]]
#         for coord in coords:
#             bp_coords.append(coord)
#
# bp_coords_xy = [i[:2] for i in bp_coords]
#
# bp_topo = []
# progress = 1
# for x in range(int(res*bp_x+1)):
#     for y in range(int(res*bp_x+1)):
#         if [x,y] not in bp_coords_xy:
#             bp_topo.append([x, y, 0])
#         progress += 1
#     print(str(round((progress / res**2)*100, 0)) + '%')
#
# bp_topo = bp_topo + bp_coords
#
# X_3d = []
# Y_3d = []
# Z_3d = []
#
# for data in bp_topo:
#     X_3d.append(data[0])
#     Y_3d.append(data[1])
#     Z_3d.append(data[2])
#
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# trisurf = ax.plot_trisurf(X_3d, Y_3d, Z_3d, cmap=cm.jet, linewidth=0.1, antialiased=True)
#
# fig.colorbar(trisurf, ax=ax, shrink=0.3, aspect=10, pad=0.15)
# ax.set_title('Surface Topology - BP')
#
# # Adding labels
# ax.set_xlabel('µm')
# ax.set_ylabel('µm')
# ax.set_zlabel('µm')
#
# ax.set_zlim(0, 50)
#
# plt.show()