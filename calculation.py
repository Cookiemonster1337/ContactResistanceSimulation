# Import
from matplotlib import pyplot as plt
from material_data import ss_14301_data


# Contact Resistance of Bottleneck.
class ContactResistance():
    cr_values = []
    f_values = range(100000, 3000000, 10000)

    def __init__(self, name, material, microcontacts, radius_1, radius2=None):
        self.name = name
        self.material = material
        self.radius_1 = radius_1
        self.diameter = 2 * radius_1
        self.microcontacts = microcontacts

    def calc_cr(self):
        self.cr_values.clear()
        for f in self.f_values:
            # bottleneck_diameter = ((0.75 * f) * (((1 - v1 ** 2) / e1)
            # + ((1 - v2 ** 2) / e2)) \* ((r1 * r2) / (r1 + r2))) ** (1 / 3)
            bottleneck_diameter = self.microcontacts * ((0.75 * f) * ((1-ss_14301_data['poisson_constant']** 2)/ss_14301_data['elastic_module']) + ((1-ss_14301_data['poisson_constant']**2)/ss_14301_data['elastic_module']) * ((self.radius_1 * self.radius_1) / (self.radius_1 + self.radius_1))) ** (1/3)
            res_bottleneck = ss_14301_data['specific_electrical_resistance'] / (2 * bottleneck_diameter)
            self.cr_values.append(res_bottleneck)
        print(self.cr_values)
        return self.cr_values

    def plot_cr(self):
        plt.plot(self.f_values, self.cr_values)
        plt.title('Theoretical Contact Resistance', pad=10)
        plt.xlabel('Contact Pressure [Pa]', labelpad=10)
        plt.ylabel('Interfacial Contact Resistivity [mOhm*cm²]', labelpad=10)

        plt.show()


sample = ContactResistance('test', 'ss14301', 1000, 1)


sample.calc_cr()
sample.plot_cr()

class ContactArea:
    pass