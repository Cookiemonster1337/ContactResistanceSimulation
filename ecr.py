import math

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