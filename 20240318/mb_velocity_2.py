#!/usr/pkg/bin/python3.12

#
# Time-stamp: <2024/03/16 19:10:56 (UT+8) daisuke>
#

# importing numpy module
import numpy

# importing scipy module
import scipy.constants

# importing matplotlib module
import matplotlib.backends.backend_agg
import matplotlib.figure

# output file name
file_output = 'mb_velocity_2.png'

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

# nitrogen molecule mass
m_n2 = 28.0 * amu

# oxygen molecule mass
m_o2 = 32.0 * amu

# argon mass
m_ar = 40.0 * amu

# carbon dioxide mass
m_co2 = 44.0 * amu

# hydrogen molecule
m_h2 = 2.0 * amu

# average temperature of the Earth surface
T = 300.0

# velocity
v = numpy.linspace (0.0, 100000.0, (10**7)+1)

# Maxwell-Boltzmann distribution
fv_n2  = calc_mbdist (v, m_n2, T)
fv_o2  = calc_mbdist (v, m_o2, T)
fv_ar  = calc_mbdist (v, m_ar, T)
fv_co2 = calc_mbdist (v, m_co2, T)
fv_h2  = calc_mbdist (v, m_h2, T)

# making a fig object
fig = matplotlib.figure.Figure ()

# making a canvas object
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)

# making an axes object
ax = fig.add_subplot (111)

# plotting data
ax.plot (v, fv_n2, \
         linestyle='-', linewidth=3, color='blue', \
         label='Nitrogen molecule')
ax.plot (v, fv_o2, \
         linestyle='-', linewidth=3, color='green', \
         label='Oxygen molecule')
ax.plot (v, fv_ar, \
         linestyle='-', linewidth=3, color='cyan', \
         label='Argon atom')
ax.plot (v, fv_co2, \
         linestyle='-', linewidth=3, color='red', \
         label='Carbon dioxide')
ax.plot (v, fv_h2, \
         linestyle='-', linewidth=3, color='magenta', \
         label='Hydrogen molecule')

# axes
ax.set_xlim (0.0, 5000.0)
ax.set_ylim (0.0, None)
ax.set_xlabel ('Velocity [m/s]')
ax.set_ylabel ('Probability')

# legend
ax.legend ()

# saving file
fig.tight_layout ()
fig.savefig (file_output, dpi=100)
