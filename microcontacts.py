import math
import matplotlib.pyplot as plt
from timeit import default_timer as timer


def find_microcontacts(gdl_params, topo_params, surface_peaks, gdl_peaks, spacing):
    # determinate max-distance
    distance_max = (gdl_params['fiber_dia [µm]'] / 2) + topo_params['r1 [µm]'] + topo_params['sigma_s [µm]']

    # generate 1D array of distances - 1µm and max_distance between baselayer of surface and gdl
    z_distance = [i for i in range(1, int(distance_max + 1))]

    # initalize arrays for data of deformation[µm], bp_contacts[x,y,z], gdl_contacts[x,y,z] depending on z-distance(pressure)
    press_rel_deformations = []
    pressure_rel_contacts_bp = []
    pressure_rel_contacts_gdl = []

    # # of contacts (digitpoints in which surface and gdl ovelap z-axis)
    n_contacts = 0

    nearest = math.inf

    print('find microcontacts depending on z-distance..')
    start = timer()
    # find overlapping/contacting areas by comparing z-axis values of gdl and surface
    for z in z_distance:
        deformations = []
        contacts_bp = []
        contacts_gdl = []
        for i in surface_peaks:

            #gdl_area = [dp for dp in gdl_peaks if dp[0] == i[0] & dp[1] == i[1]]
            for j in gdl_peaks: #TODO: specify range to smaller array within given range of surface peak
                delta_x = abs(j[0] - i[0])
                delta_y = abs(j[1] - i[1])
                asperity_height = i[2] - topo_params['r1 [µm]']  # TODO: ?
                distance_2d = math.sqrt(delta_x ** 2 + delta_y ** 2)
                distance_3d = math.sqrt(distance_2d ** 2 + (z - asperity_height) ** 2)
                if distance_3d < distance_max:
                    n_contacts += 1 #TODO: does trigger even when 2d != nearest
                    if distance_2d < nearest:
                        nearest = distance_2d
                        deformation = distance_max - distance_3d
                        nearest_i = i
                        nearest_j = j
            if nearest < math.inf:
                deformations.append(deformation)
                contacts_bp.append(nearest_i)
                contacts_gdl.append(nearest_j)
            nearest = math.inf
        press_rel_deformations.append(deformations)
        pressure_rel_contacts_bp.append(contacts_bp)
        pressure_rel_contacts_gdl.append(contacts_gdl)
    end = timer()
    print(str(n_contacts) + ' microcontacts found!' + '(' + str(round(end - start, 2)) + 's)')

    return press_rel_deformations, pressure_rel_contacts_bp, pressure_rel_contacts_gdl

def microcontacts_2d(pressure_mc_bp):
    bp_contacts_x = []
    bp_contacts_y = []
    gdl_contacts_x = []
    gdl_contacts_y = []

    for i in pressure_mc_bp[6]:
        bp_contacts_x.append(i[0])
        bp_contacts_y.append(i[1])

    plt.scatter(bp_contacts_x, bp_contacts_y, 0.1)

    plt.show()

