import random
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from timeit import default_timer as timer
import pandas as pd
from pymongo import MongoClient
import numpy as np
from scipy.interpolate import griddata
import plotly.graph_objects as go



def create_surfacetopo(res, area, surface_params):

    r1 = surface_params['r1 [µm]']
    dpeak = surface_params['d_peak [1/mm]']
    sigma = surface_params['sigma_s [µm]']

    # length x,y axis
    length_xy = math.sqrt(area)
    # datapoints along single axis element
    digits_xy = int(res * length_xy + 1)

    # xy-basis-mesh
    mesh_basis = [[x, y] for x in range(digits_xy) for y in range(digits_xy)] #TODO: speed up possibilities?

    # initalize peakdata-list
    peaks_2d = []
    # get no. of peaks
    peak_no = int((dpeak * length_xy) ** 2)

    # generate peaks (origin and area) !only xy-coordinates
    print('start peak-randomization...')
    start = timer()
    for i in range(peak_no + 1):
        peak = random.choice(mesh_basis)    # set random coordinates for peak origin
        peaks_2d.append(peak)  # add peak coordinates to list
        # determine xy-area of peak depending on asperity radius
        peak_xrange = range(peak[0] - int(r1), peak[0] + int(r1 + 1))
        peak_yrange = range(peak[1] - int(r1), peak[1] + int(r1 + 1))
        peak_square = [[x, y] for x in peak_xrange for y in peak_yrange]
        # add xy-area of peak to mesh-baselayer
        mesh_basis = [xy for xy in mesh_basis if xy not in peak_square]
        # clear peakdata for next loop
        peak_square.clear()
    end = timer()
    print('peak-positions generated!' + '(' + str(round(end-start, 2)) + 's)')
    # mesh for 3d data (x,y,z)
    surface_peaks = []
    surface_mean_summit = []

    # generate random z-coordinate in given range (sigma_s, r1) for every peak
    print('start peak-height determination')
    start = timer()
    for peak in peaks_2d:
        # find random height (z-coordinate) within given range defined by sigma_s and r1
        # h = round(random.uniform(surface_params['r1 [µm]'] - (surface_params['sigma_s [µm]'] / 2), surface_params['r1 [µm]'] +
        #                          (surface_params['sigma_s [µm]'] / 2)), 2)
        h = round(random.uniform(0, 2 * sigma), 2)
        hr = h + r1
        # add 3D-peak-coordinate (x,y,z) of !peak-origin to surface-mesh
        surface_peaks.append([peak[0], peak[1], hr])
        surface_mean_summit.append([peak[0], peak[1], h])
        # generate spherical shape of whole peak over corresponding peak-area
        for i in range(1, int(r1)): #TODO: +1?
            # calculate z-coordinate corresponding to lateral distance between i and peak-origin (spherical shape)
            z = round(math.sin(math.acos(i / hr)) * hr, 2)
            # create surface mesh of single peak with resulting datapoints (surrounding peak-origin)
            peaks_3d = [[peak[0] - i, peak[1], z], [peak[0] + i, peak[1], z], [peak[0], peak[1] - i, z],
                      [peak[0], peak[1] + i, z],
                      [peak[0] + 1, peak[1] + i, z], [peak[0] + i, peak[1] - i, z], [peak[0] - i, peak[1] + i, z],
                      [peak[0] - i, peak[1] - i, z]]
            # for every additional digit-step away from peak-origin more datapoints (greater surroundings) need to be added
            if i > 1:
                for a in range(1, i):
                    peaks_3d += [[peak[0] + i, peak[1] + a, z], [peak[0] + i, peak[1] - a, z],
                                [peak[0] - i, peak[1] + a, z], [peak[0] - i, peak[1] - a, z],
                                [peak[0] + a, peak[1] + i, z], [peak[0] - a, peak[1] + i, z],
                                [peak[0] + a, peak[1] - i, z], [peak[0] - a, peak[1] - i, z]]
            for coord in peaks_3d: #TODO: review way of processing data
                surface_peaks.append(coord)
    end = timer()
    print('peak-height generated!' + '(' + str(round(end-start, 2)) + 's)')

    print('generate empty mesh...')
    start = timer()
    # xy-data of mesh_surface
    mesh_surface_xy = [i[:2] for i in surface_peaks]
    end = timer()
    print('empty mesh generated!' + '(' + str(round(end-start, 2)) + 's)')

    # fill mesh_surface with 0-level
    start = timer()
    print('start filling surface mesh...')
    surface = []
    for x in range(digits_xy):
        for y in range(digits_xy):
            if [x, y] not in mesh_surface_xy:
                surface.append([x, y, 0])
    surface = surface + surface_peaks
    end = timer()
    print('surface successfully generated!' + '(' + str(round(end-start, 2)) + 's)')

    # surface-data-dictionary
    surface_data = {'area [mm^2]': area, 'xy-length [mm]': length_xy, 'xy-datapoints [#]': digits_xy,
                    'peaks [#]': peak_no, 'peaks [x,y,z]': surface_peaks, 'surface [x,y,z]': surface}

    surface_df = pd.DataFrame(surface, columns=['x_val', 'y_val', 'z_val'])
    filename = 'surface_' + str(surface_params['d_peak [1/mm]']) + '_' + str(surface_params['r1 [µm]']) + '_' + str(surface_params['sigma_s [µm]']) + '.csv'
    surface_df.to_csv('data/surface/' + filename, sep='\t')

    # initialize mongo connector object with ip adress
    client = MongoClient('zbts07')
    # get reference to existing database testDB
    db = client.testDB
    # reference collection, if not existent it will be created
    current_collection = db['NMT_TestCollection']
    # authentication within database
    db.authenticate('jkp', 'qwertz', source='admin')

    current_collection.insert_one(surface_data)

    return surface, surface_peaks, surface_data, surface_mean_summit

# def create_surfacetopo(res, area, surface_params):
#
#     # length x,y axis
#     length_xy = math.sqrt(area)
#     # datapoints along single axis element
#     digits_xy = int(res * length_xy + 1)
#
#     # xy-basis-mesh
#     mesh_basis = [[x, y] for x in range(digits_xy) for y in range(digits_xy)] #TODO: speed up possibilities?
#
#     # initalize peakdata-list
#     peaks_2d = []
#     # get no. of peaks
#     peak_no = int((surface_params['d_peak [1/mm]'] * length_xy) ** 2)
#
#     # generate peaks (origin and area) !only xy-coordinates
#     print('start peak-randomization...')
#     start = timer()
#     for i in range(peak_no + 1):
#         peak = random.choice(mesh_basis)    # set random coordinates for peak origin
#         peaks_2d.append(peak)  # add peak coordinates to list
#         # determine xy-area of peak depending on asperity radius
#         peak_xrange = range(peak[0] - int(surface_params['r1 [µm]']), peak[0] + int(surface_params['r1 [µm]'] + 1))
#         peak_yrange = range(peak[1] - int(surface_params['r1 [µm]']), peak[1] + int(surface_params['r1 [µm]'] + 1))
#         peak_square = [[x, y] for x in peak_xrange for y in peak_yrange]
#         # add xy-area of peak to mesh-baselayer
#         mesh_basis = [xy for xy in mesh_basis if xy not in peak_square]
#         # clear peakdata for next loop
#         peak_square.clear()
#     end = timer()
#     print('peak-positions generated!' + '(' + str(round(end-start, 2)) + 's)')
#     # mesh for 3d data (x,y,z)
#     surface_peaks = []
#
#     # generate random z-coordinate in given range (sigma_s, r1) for every peak
#     print('start peak-height determination')
#     start = timer()
#     for peak in peaks_2d:
        # find random height (z-coordinate) within given range defined by sigma_s and r1
        # h = round(random.uniform(surface_params['r1 [µm]'] - (surface_params['sigma_s [µm]'] / 2), surface_params['r1 [µm]'] +
        #                          (surface_params['sigma_s [µm]'] / 2)), 2)
#         # add 3D-peak-coordinate (x,y,z) of !peak-origin to surface-mesh
#         surface_peaks.append([peak[0], peak[1], h])
#         # generate spherical shape of whole peak over corresponding peak-area
#         for i in range(1, int(h)): #TODO: +1?
#             # calculate z-coordinate corresponding to lateral distance between i and peak-origin (spherical shape)
#             z = round(math.sin(math.acos(i / h)) * h, 2)
#             # create surface mesh of single peak with resulting datapoints (surrounding peak-origin)
#             peaks_3d = [[peak[0] - i, peak[1], z], [peak[0] + i, peak[1], z], [peak[0], peak[1] - i, z],
#                       [peak[0], peak[1] + i, z],
#                       [peak[0] + 1, peak[1] + i, z], [peak[0] + i, peak[1] - i, z], [peak[0] - i, peak[1] + i, z],
#                       [peak[0] - i, peak[1] - i, z]]
#             # for every additional digit-step away from peak-origin more datapoints (greater surroundings) need to be added
#             if i > 1:
#                 for a in range(1, i):
#                     peaks_3d += [[peak[0] + i, peak[1] + a, z], [peak[0] + i, peak[1] - a, z],
#                                 [peak[0] - i, peak[1] + a, z], [peak[0] - i, peak[1] - a, z],
#                                 [peak[0] + a, peak[1] + i, z], [peak[0] - a, peak[1] + i, z],
#                                 [peak[0] + a, peak[1] - i, z], [peak[0] - a, peak[1] - i, z]]
#             for coord in peaks_3d: #TODO: review way of processing data
#                 surface_peaks.append(coord)
#     end = timer()
#     print('peak-height generated!' + '(' + str(round(end-start, 2)) + 's)')
#
#     print('generate empty mesh...')
#     start = timer()
#     # xy-data of mesh_surface
#     mesh_surface_xy = [i[:2] for i in surface_peaks]
#     end = timer()
#     print('empty mesh generated!' + '(' + str(round(end-start, 2)) + 's)')
#
#     # fill mesh_surface with 0-level
#     start = timer()
#     print('start filling surface mesh...')
#     surface = []
#     for x in range(digits_xy):
#         for y in range(digits_xy):
#             if [x, y] not in mesh_surface_xy:
#                 surface.append([x, y, 0])
#     surface = surface + surface_peaks
#     end = timer()
#     print('surface successfully generated!' + '(' + str(round(end-start, 2)) + 's)')
#
#     # surface-data-dictionary
#     surface_data = {'area [mm^2]': area, 'xy-length [mm]': length_xy, 'xy-datapoints [#]': digits_xy,
#                     'peaks [#]': peak_no, 'peaks [x,y,z]': surface_peaks, 'surface [x,y,z]': surface}
#
#     surface_df = pd.DataFrame(surface, columns=['x_val', 'y_val', 'z_val'])
#     filename = 'surface_' + str(surface_params['d_peak [1/mm]']) + '_' + str(surface_params['r1 [µm]']) + '_' + str(surface_params['sigma_s [µm]']) + '.csv'
#     surface_df.to_csv('data/surface/' + filename, sep='\t')
#
#     # initialize mongo connector object with ip adress
#     client = MongoClient('zbts07')
#     # get reference to existing database testDB
#     db = client.testDB
#     # reference collection, if not existent it will be created
#     current_collection = db['NMT_TestCollection']
#     # authentication within database
#     db.authenticate('jkp', 'qwertz', source='admin')
#
#     current_collection.insert_one(surface_data)
#
#     return surface, surface_peaks, surface_data


def surfacetopo_3d(res, surfacetopo, zlim):
    start = timer()
    print('start generating z-array for plot...')
    X_3d = []
    Y_3d = []
    Z_3d = []

    for data in surfacetopo:
        X_3d.append(data[0])
        Y_3d.append(data[1])
        Z_3d.append(data[2])

    end = timer()
    print('z-array generated!' + '(' + str(round(end - start, 2)) + 's)')

    # print('plot matplotlib...')
    # start = timer()
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
    # ax.set_zlim(0, zlim)
    #
    # end = timer()
    # print('matplotlib plotted!' + '(' + str(round(end - start, 2)) + 's)')
    # plt.show()


    print('plot plotly...')
    start = timer()
    xi = np.linspace(1, 100, 100)
    yi = np.linspace(1, 100, 100)

    X, Y = np.meshgrid(xi, yi)

    Z = griddata((X_3d, Y_3d), Z_3d, (X, Y), method='cubic')

    # plt.pcolormesh(X, Y, Z)
    # plt.show()

    fig = go.Figure(data=[go.Surface(z=Z)])

    fig.update_layout(title='surface', scene=dict(xaxis_title='x [µm]', yaxis_title=' y [µm]', zaxis_title='z [µm]',
                                                  zaxis=dict(nticks=4, range=[0, 50])))
    end = timer()
    print('plotly plotted!' + '(' + str(round(end - start, 2)) + 's)')
    fig.show()

    return X_3d, Y_3d, Z_3d, X, Y

def surface_crosssection_2d(surfacetopo, xpos):
    crosssection = []
    Y_2d = []
    Z_2d = []


    for data in surfacetopo:
        if data[0] == xpos:
            crosssection.append([data[1], data[2]])

    crosssection.sort()

    for data in crosssection:
        Y_2d.append(data[0])
        Z_2d.append(data[1])

    plt.ylim(0, 20)
    plt.plot(Y_2d, Z_2d, 0.1)

    plt.title("cross section @xpos: " + str(xpos) + 'µm')
    plt.xlabel("µm")
    plt.ylabel("µm")

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