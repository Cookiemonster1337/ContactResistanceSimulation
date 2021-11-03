import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
from surface import create_surfacetopo, surfacetopo_3d
from fibers import create_gdltopo, gdltopo_3d

res = 1000 #µm/mm

area = 0.01 #mm2

pressure = 1 #MPa

topo_params = {'d_peak': 200, 'r1': 2, 'sigma_s': 5} #TODO: add units
gdl_params = {'gdl_thk [µm]': 110, 'porosity': 0.7, 'fiber_dia [µm]': 7, 'binder_thk [µm]': 6}

surface, surface_peaks = create_surfacetopo(res, area, topo_params)
surfacetopo_3d(surface)

gdl, gdl_peaks = create_gdltopo(res, area, gdl_params)
gdltopo_3d(gdl)

distance_max = (gdl_params['fiber_dia [µm]'] / 2) + topo_params['r1'] + topo_params['sigma_s']
distance_z = distance_max * ((10-pressure)/10) #TODO: find relation pressure <--> distance

n_contacts = 0
contacts = []
distance_2d = 0
nearest = 10000

for i in surface_peaks:
    if nearest < 10000:
        contacts.append(nearest_i + nearest_j)
    nearest = 10000
    for j in gdl_peaks:
        delta_x = abs(j[0] - i[0])
        delta_y = abs(j[1] - i[1])
        asperity_height = i[2] - topo_params['r1']
        distance_2d = math.sqrt(delta_x ** 2 + delta_y ** 2)
        distance_3d = math.sqrt(distance_2d ** 2 + (distance_z - asperity_height) ** 2)
        if distance_3d < distance_max:
            n_contacts += 0
            if distance_2d < nearest:
                nearest = distance_2d
                nearest_i = i
                nearest_j = j

print(contacts)
