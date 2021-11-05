import math
import matplotlib.pyplot as plt


def find_microcontacts(gdl_params, topo_params, surface_peaks, gdl_peaks):
    distance_max = (gdl_params['fiber_dia [µm]'] / 2) + topo_params['r1 [µm]'] + topo_params['sigma_s [µm]']
    z_distance = [i for i in range(1, int(distance_max + 1))]
    pressure_mc = []
    pressure_mc_bp = []
    pressure_mc_gdl = []
    n_contacts = 0
    nearest = 10000

    for z in z_distance:
        microcontacts = []
        microcontacts_bp = []
        microcontacts_gdl = []
        for i in surface_peaks:
            if nearest < 10000:
                microcontacts.append(deformation)
                microcontacts_bp.append(nearest_i)
                microcontacts_gdl.append(nearest_j)
            nearest = 10000
            for j in gdl_peaks:
                delta_x = abs(j[0] - i[0])
                delta_y = abs(j[1] - i[1])
                asperity_height = i[2] - topo_params['r1 [µm]']  # TODO: ?
                distance_2d = math.sqrt(delta_x ** 2 + delta_y ** 2)
                distance_3d = math.sqrt(distance_2d ** 2 + (z - asperity_height) ** 2)
                if distance_3d < distance_max:
                    n_contacts += 1
                    if distance_2d < nearest:
                        nearest = distance_2d
                        deformation = distance_max - distance_3d
                        nearest_i = i
                        nearest_j = j

        pressure_mc.append(microcontacts)
        pressure_mc_bp.append(microcontacts_bp)
        pressure_mc_gdl.append(microcontacts_gdl)

    return pressure_mc, pressure_mc_bp, pressure_mc_gdl

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

