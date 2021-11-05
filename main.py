from surface import create_surfacetopo, surfacetopo_3d, surface_crosssection_2d
from fibers import create_gdltopo, gdltopo_3d, gdltopo_2d, gdlpeaks_2d, gdl_crosssection_2d
from microcontacts import find_microcontacts, microcontacts_2d
from ecr import calc_ecr, plot_ecr
from pymongo import MongoClient

# initialize mongo connector object with ip adress
client = MongoClient('zbts07')
# get reference to existing database testDB
db = client.testDB
# reference collection, if not existent it will be created
current_collection = db['NMT_TestCollection']
# authentication within database
db.authenticate('jkp', 'qwertz', source='admin')

# main parameters
res = 1000 #µm/mm
area = 0.01 #mm2
pressure = 1 #MPa

surface_params = {'d_peak [1/mm]': 100, 'r1 [µm]': 3.67, 'sigma_s [µm]': 3.55}
gdl_params = {'gdl_thk [µm]': 110, 'porosity': 0.7, 'fiber_dia [µm]': 7, 'binder_thk [µm]': 6}

gdl_mat_props = {'el. res. [µOhm*m]': 800}
surface_mat_props = {'el. res. [µOhm*m]': 190}

surface, surface_peaks, surface_data = create_surfacetopo(res, area, surface_params)
surfacetopo_3d(surface, 50)

#surface_crosssection_2d(surface_peaks, 50)

gdl, gdl_peaks, gdl_fibers = create_gdltopo(res, area, gdl_params)
# gdltopo_2d(gdl_fibers)
# gdlpeaks_2d(gdl_peaks)
# gdl_crosssection_2d(gdl, 50)

mcs, mcs_surface, mcs_gdl = find_microcontacts(gdl_params, surface_params, surface_peaks, gdl_peaks)
# microcontacts_2d(mcs_surface)

ecr, z_distance = calc_ecr(gdl_params, surface_params, surface_mat_props, gdl_mat_props, mcs)


gdltopo_3d(gdl)
plot_ecr(ecr, z_distance)




