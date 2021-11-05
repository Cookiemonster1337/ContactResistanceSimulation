from surface import create_surfacetopo, surfacetopo_3d, surface_crosssection_2d

res = 1000 #µm/mm
area = 0.01 #mm2
pressure = 1 #MPa

surface_params = {'d_peak [1/mm]': 200, 'r1 [µm]': 2.5, 'sigma_s [µm]': 5}
gdl_params = {'gdl_thk [µm]': 110, 'porosity': 0.7, 'fiber_dia [µm]': 7, 'binder_thk [µm]': 6}

gdl_mat_props = {'el. res. [µOhm*m]': 800}
surface_mat_props = {'el. res. [µOhm*m]': 190}

surface, surface_peaks, surface_data = create_surfacetopo(res, area, surface_params)
surfacetopo_3d(surface, 500)
surface_crosssection_2d(surface, 50)

