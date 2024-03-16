#!/usr/pkg/bin/python3.12

#
# Time-stamp: <2024/03/16 19:06:16 (UT+8) daisuke>
#

# importing argparse module
import argparse

# importing numpy module
import numpy

# importing scipy module
import scipy.constants

# importing matplotlib module
import matplotlib.backends.backend_agg
import matplotlib.figure

# initialising a parser
descr  = f'Maxwell-Boltzmann velocity distribution'
parser = argparse.ArgumentParser (description=descr)

# adding arguments
parser.add_argument ('-a', '--vmin', type=float, default=0.0, \
                     help='minimum velocity to plot in m/s (default: 0)')
parser.add_argument ('-b', '--vmax', type=float, default=3000.0, \
                     help='maximum velocity to plot in m/s (default: 3000)')
parser.add_argument ('-m', '--mass', type=float, default=28.0, \
                     help='molecular mass in dalton (default: 28)')
parser.add_argument ('-n', '--name', default='nitrogen molecule', \
                     help='name of gas particle (default: nitrogen molecule)')
parser.add_argument ('-o', '--output', default='plot.png', \
                     help='output file name (default: plot.png)')
parser.add_argument ('-r', '--resolution', type=float, default=225.0, \
                     help='resolution of output file in DPI (default: 225)')
parser.add_argument ('-t', '--temperature', type=float, default=300.0, \
                     help='temperature in K (default: 300)')

# parsing arguments
args = parser.parse_args ()

# input parameters
v_min          = args.vmin
v_max          = args.vmax
molecular_mass = args.mass
gas_species    = args.name
file_output    = args.output
resolution_dpi = args.resolution
temperature    = args.temperature

# value of pi
pi = scipy.constants.pi

# Boltzmann constant
k = scipy.constants.k

# atomic mass unit
amu = scipy.constants.physical_constants['atomic mass constant'][0]

# function to calculate Maxwell-Boltzmann distribution
def calc_mbdist (v, m, T):
    # probability of having velocity v
    f = (m / (2.0 * pi * k * T) )**1.5 \
        * 4.0 * pi * v**2 \
        * numpy.exp (-1.0 * m * v**2 / (2.0 * k * T) )
    # returning f
    return f

# mass of a gas particle in kg
mass_kg = molecular_mass * amu

# velocity
v = numpy.linspace (0.0, 100000.0, (10**7)+1)

# Maxwell-Boltzmann distribution
fv = calc_mbdist (v, mass_kg, temperature)

# making a fig object
fig = matplotlib.figure.Figure ()

# making a canvas object
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)

# making an axes object
ax = fig.add_subplot (111)

# plotting data
ax.plot (v, fv, \
         linestyle='-', linewidth=3, color='red', \
         label=gas_species)

# axes
ax.set_xlim (v_min, v_max)
ax.set_ylim (0.0, None)
ax.set_xlabel ('Velocity [m/s]')
ax.set_ylabel ('Probability')
ax.grid ()

# legend and text
ax.legend ()
label_temperature = f'temperature: {temperature:5.1f} K'
ax.text (0.95, 0.30, label_temperature, \
         horizontalalignment='right', transform=ax.transAxes)
label_mass = f'molecular mass: {molecular_mass} Da'
ax.text (0.95, 0.25, label_mass, \
         horizontalalignment='right', transform=ax.transAxes)

# saving file
fig.tight_layout ()
fig.savefig (file_output, dpi=resolution_dpi)
