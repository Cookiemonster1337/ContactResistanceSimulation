import random
import math
import matplotlib.pyplot as plt



# parameters
d_peak = 20 #98
r1 = 3.67
sigma_s =  3.55
area = 0.1 #mm2
res = int(1000 * area)


# three-dimensional-array
mesh = [[x,y] for x in range(0, res+1) for y in range(0, res+1)]

# peak-distribution
peak_square = []
peaks = []
peak_count = d_peak**2

for i in range(peak_count+1):
    #print(str(round(i / (peak_count+1) * 100, 2)) + ' %')
    peak = random.choice(mesh)
    peaks.append(peak)
    peak_xrange = range(peak[0] - int(r1), peak[0] + int(r1+1))
    peak_yrange = range(peak[1] - int(r1), peak[1] + int(r1+1))
    peak_square = [[x,y] for x in peak_xrange for y in peak_yrange]
    mesh = [xy for xy in mesh if xy not in peak_square]
    peak_square.clear()

# height-distribution
bp_coords = [] # 3D-coordinates for peaks
progress = 0
bp_peaks = []

for peak in peaks:
    progress += 1
    #print(str(round(progress/(len(peaks)) * 100, 2)) + ' %')
    h = round(random.uniform(r1-(sigma_s/2), r1 + (sigma_s/2)), 2) #height of peak in given simga_s
    bp_coords.append([peak[0], peak[1], h])
    bp_peaks.append([peak[0], peak[1], h])
    for i in range(1, int(h+1)): #spherical shape
        z = round(math.sin(math.acos(i/h)) * h, 2)
        coords = [[peak[0]-i, peak[1], z], [peak[0]+i, peak[1], z], [peak[0], peak[1]-i, z], [peak[0], peak[1]+i, z],
                  [peak[0]+1, peak[1]+i, z], [peak[0]+i, peak[1]-i, z], [peak[0]-i, peak[1]+i, z], [peak[0]-i, peak[1]-i, z]]
        if i > 1:
            for a in range(1,i):
                coords += [[peak[0]+i, peak[1]+a, z], [peak[0]+i, peak[1]-a, z], [peak[0]-i, peak[1]+a, z], [peak[0]-i, peak[1]-a, z],
                [peak[0]+a, peak[1]+i, z], [peak[0]-a, peak[1]+i, z], [peak[0]+a, peak[1]-i, z], [peak[0]-a, peak[1]-i, z]]
        for coord in coords:
            bp_coords.append(coord)

# fill up topography
bp_coords_xy = [i[:2] for i in bp_coords]

bp_topo = []
progress = 1
for x in range(res+1):
    for y in range(res+1):
        if [x,y] not in bp_coords_xy:
            bp_topo.append([x, y, 0])
        progress += 1
    #print(str(round((progress / res**2)*100, 0)) + '%')

bp_topo = bp_topo + bp_coords

print(bp_topo[:5])



# parameters
gdl_thk = 110  # µm
por_vol = 0.7
fiber_dia = 7  # µm
binder_thk = 6  # µm

gdl_vol = gdl_thk * 10 ** -6 * area * 10 ** -3 * area * 10 ** -3

tot_fiber_len = (gdl_vol * (1 - por_vol)) / (0.25 * math.pi * (fiber_dia * 10 ** -6) ** 2)
layer_num = gdl_thk / (fiber_dia + binder_thk)
layer_fiber_len = tot_fiber_len / layer_num

# three dimensional array
res = int(area * 1000)
mesh = [[x, y, 0] for x in range(0, res + 1) for y in range(0, res + 1)]

# gdl fiber distribution
gdl_coords = []
gdl_peaks = []
fiber_len = int(layer_fiber_len * 1 * 10 ** 6)
h = fiber_dia


def fiber_coords_y(datapoint, d):
    gdl_coords.append(datapoint)
    gdl_peaks.append(datapoint)
    for i in range(1, int(d / 2) + 1):
        z = round(math.sin(math.acos(i / h)) * h, 2)
        datapoint_up = [datapoint[0], datapoint[1] + i, z]
        gdl_coords.append(datapoint_up)
        datapoint_down = [datapoint[0], datapoint[1] - i, z]
        gdl_coords.append(datapoint_down)


def fiber_coords_x(datapoint, d):
    gdl_coords.append(datapoint)
    gdl_peaks.append(datapoint)
    for i in range(1, int(d / 2)):
        z = round(math.sin(math.acos(i / h)) * h, 2)
        datapoint_up = [datapoint[0] + i, datapoint[1], z]
        gdl_coords.append(datapoint_up)
        datapoint_down = [datapoint[0] - i, datapoint[1], z]
        gdl_coords.append(datapoint_down)


def fiber_path(p, direction, fiber_len):
    if direction == 0:
        while p[0] in range(res + 1) and p[1] in range(res + 1) and fiber_len > 0:
            p = [p[0] + 1, p[1] + 0, h]
            fiber_len += -1
            fiber_coords_y(p, fiber_dia)
    elif direction == 1:
        while p[0] in range(res + 1) and p[1] in range(res + 1) and fiber_len > 0:
            p = [p[0] + 1, p[1] + 1, h]
            fiber_len += -1.4142
            fiber_coords_y(p, fiber_dia)
    elif direction == 2:
        while p[0] in range(res + 1) and p[1] in range(res + 1) and fiber_len > 0:
            p = [p[0] + 1, p[1] - 1, h]
            fiber_len += -1.4142
            fiber_coords_y(p, fiber_dia)
    elif direction == 3:
        while p[0] in range(res + 1) and p[1] in range(res + 1) and fiber_len > 0:
            p = [p[0] + 1, p[1] + 2, h]
            fiber_len += -1.7321
            fiber_coords_y(p, fiber_dia)
    elif direction == 4:
        while p[0] in range(res + 1) and p[1] in range(res + 1) and fiber_len > 0:
            p = [p[0] + 1, p[1] - 2, h]
            fiber_len += -1.7321
            fiber_coords_y(p, fiber_dia)
    elif direction == 5:
        while p[0] in range(res + 1) and p[1] in range(res + 1) and fiber_len > 0:
            p = [p[0] + 2, p[1] - 1, h]
            fiber_len += -1.7321
            fiber_coords_y(p, fiber_dia)
    elif direction == 6:
        while p[0] in range(res + 1) and p[1] in range(res + 1) and fiber_len > 0:
            p = [p[0] - 2, p[1] - 1, h]
            fiber_len += -1.7321
            fiber_coords_y(p, fiber_dia)
    return fiber_len


while fiber_len > 0:
    start = random.randint(0, 4)
    if start == 0:
        p = [0, random.randint(1, res + 1), h]
        fiber_coords_y(p, fiber_dia)
        direction = random.randint(0, 7)
        fiber_len = fiber_path(p, direction, fiber_len)
    elif start == 1:
        p = [random.randint(1, res + 1), res, h]
        fiber_coords_x(p, fiber_dia)
        direction = random.randint(0, 3)
        fiber_len = fiber_path(p, direction, fiber_len)
    elif start == 2:
        p = [res, random.randint(1, res + 1), h]
        fiber_coords_y(p, fiber_dia)
        direction = random.randint(0, 3)
        fiber_len = fiber_path(p, direction, fiber_len)
    elif start == 3:
        p = [random.randint(1, res + 1), 0, h]
        fiber_coords_x(p, fiber_dia)
        direction = random.randint(0, 3)
        fiber_len = fiber_path(p, direction, fiber_len)

# fill up topography
gdl_coords_xy = [i[:2] for i in gdl_coords]
# print(len(gdl_coords_xy))

mesh = []
progress = 1
for x in range(res + 1):
    for y in range(res + 1):
        if [x, y] not in gdl_coords_xy:
            mesh.append([x, y, 0])
        progress += 1
    # print(str(round((progress / res**2)*100, 0)) + '%')

gdl_topo = mesh + gdl_coords





r_fiber = fiber_dia / 2
max_seperation = r1 + sigma_s + r_fiber
separations = [i for i in range(1, int(max_seperation + 1))]
pressure_mc = []
pressure_mc_bp = []
pressure_mc_gdl = []
max_distance = r_fiber + r1
n_contacts = 0
distance_2d = 0
nearest = 10000

for pressure in separations:
    microcontacts = []
    microcontacts_bp = []
    microcontacts_gdl = []
    for i in bp_peaks:
        if nearest < 10000:
            microcontacts.append(deformation)
            microcontacts_bp.append(nearest_i)
            microcontacts_gdl.append(nearest_j)
        nearest = 10000
        for j in gdl_peaks:
            delta_x = abs(j[0] - i[0])
            delta_y = abs(j[1] - i[1])
            asperity_height = i[2] - r1
            distance_2d = math.sqrt(delta_x ** 2 + delta_y ** 2)
            distance_3d = math.sqrt(distance_2d ** 2 + (pressure - asperity_height) ** 2)
            if distance_3d < max_distance:
                n_contacts += 0
                if distance_2d < nearest:
                    nearest = distance_2d
                    deformation = max_distance - distance_3d
                    nearest_i = i
                    nearest_j = j

    pressure_mc.append(microcontacts)
    pressure_mc_bp.append(microcontacts_bp)
    pressure_mc_gdl.append(microcontacts_gdl)