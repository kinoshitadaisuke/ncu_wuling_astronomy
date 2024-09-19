#!/usr/pkg/bin/python3.12

#
# Time-stamp: <2024/09/19 20:04:49 (UT+8) daisuke>
#

# importing numpy module
import numpy

# importing scipy module
import scipy.constants

# importing matplotlib module
import matplotlib.backends.backend_agg
import matplotlib.figure

# value of pi
pi = scipy.constants.pi

# Boltzmann constant
k = scipy.constants.k

# atomic mass unit
amu = scipy.constants.physical_constants['atomic mass constant'][0]

# nitrogen molecule mass
m_n2 = 28.0 * amu

# average temperature of the Earth surface
T_earth = 300.0

# function to calculate Maxwell-Boltzmann distribution
def calc_mbdist (v, m, T):
    # probability of having velocity v
    f = (m / (2.0 * pi * k * T) )**1.5 \
        * 4.0 * pi * v**2 \
        * numpy.exp (-1.0 * m * v**2 / (2.0 * k * T) )
    # returning f
    return f

# root-mean-square velocity
v_rms = numpy.sqrt (3.0 * k * T_earth / m_n2)

# range of integration
v_min = 6.0 * v_rms
v_max = numpy.infty

# numerical integration
result = scipy.integrate.quad (calc_mbdist, v_min, v_max, args=(m_n2, T_earth) )

# printing result
print (f'result = {result}')
