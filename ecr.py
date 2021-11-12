import math
import matplotlib.pyplot as plt

contact_area_x = 1000 #µm
contact_area_y = 1000 #µm

gdl_distance = 7.5 #µm
fiber_dia = 7 #µm
asperity_r = 7 #µm varies betwenn given range of sigma_s
deformation = gdl_distance - asperity_r #µm

poisson_ratio_bp = 0.3 #stainless-steel (wikipedia/poisson-ratio)
poisson_ratio_gdl = 0 #assumption made due to high stiffness of carbon fibers nad high porosity of material (eg. multi-physics-modeling of the anode of liquid-feed methanol fuel cells)

young_mod_bp = 10 #GPa
young_mod_gdl = 3.2 #GPa

res_bp = 190 #µOhm*m
res_gdl = 800 #µOhm*m

fiber_r = fiber_dia/2

young_mod = (((1 - poisson_ratio_bp**2) / young_mod_bp) + ((1 - poisson_ratio_gdl**2) / young_mod_gdl))**(-1)
equivalent_r = asperity_r * math.sqrt(fiber_r/ (asperity_r + fiber_r))

contact_area = math.pi * equivalent_r * deformation
contact_load = (4/3) * young_mod * equivalent_r**(1/2) * deformation**(3/2)

con_area = math.pi * asperity_r * (math.sqrt(fiber_r/(asperity_r + fiber_r))) * deformation

con_area_r = math.sqrt(con_area / math.pi)

ecr = (res_bp + res_gdl) / (4 * con_area_r)


def calc_ecr(gdl_params, topo_params, surface_mat_props, gdl_mat_props, mcs):
    # define arrays for microcontacts (mc) and electrical contact resistances (ecr)
    mc_ecr = []
    ecr_series = []

    # determinate max-distance between gdl- and surface-baselayer in which ecr calculation is still relevant
    distance_max = (gdl_params['fiber_dia [µm]'] / 2) + topo_params['r1 [µm]'] + topo_params['sigma_s [µm]']

    # generate 1D array of distances - 1µm and max_distance between baselayer of surface and gdl
    z_distance = [i for i in range(1, int(distance_max + 1))]

    # find overlapping/contacting (microcontacts) areas by comparing z-axis values of gdl and surface for different z-distances (pressures)
    for pressure in mcs:
        for mc in pressure:
            deformation = mc

            con_area = math.pi * topo_params['r1 [µm]'] * \
                       (math.sqrt((gdl_params['fiber_dia [µm]'] / 2) / (topo_params['r1 [µm]'] +
                                                                        (gdl_params[
                                                                             'fiber_dia [µm]'] / 2)))) * deformation

            con_area_r = math.sqrt(con_area / math.pi)

            ecr = (surface_mat_props['el. res. [µOhm*m]'] + gdl_mat_props['el. res. [µOhm*m]']) / (
                        4 * (con_area_r * 10 ** -6))

            mc_ecr.append(ecr)

        area_ecr = 0
        for i in mc_ecr:
            area_ecr += (1 / i)
        area_ecr = (area_ecr ** -1) * 10 ** -3  # mOhm

        ecr_series.append(round(area_ecr, 2))

    return ecr_series, z_distance

def plot_ecr(ecr_series, z_distance):
    plt.plot(z_distance, ecr_series)

    plt.show()
