#!/usr/pkg/bin/python3.10

#
# Time-stamp: <2023/09/14 12:03:47 (CST) daisuke>
#

# importing argparse module
import argparse

# importing numpy module
import numpy

# importing scipy module
import scipy.constants

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# initialising a parser
parser = argparse.ArgumentParser (description='blackbody radiation')

# adding arguments
parser.add_argument ('-o', '--output', default='blackbody_radiation.png', \
                     help='name of output file')
parser.add_argument ('temperature', nargs='+', type=float, default='5800', \
                     help='temperature in K (default: 5800)')

# parsing arguments
args = parser.parse_args ()

# parameters
file_output      = args.output
list_temperature = args.temperature

#
# function to calculate blackbody curve
#
def bb_lambda (wavelength, T):
    # speed of light
    c = scipy.constants.physical_constants['speed of light in vacuum']

    # Planck constant
    h = scipy.constants.physical_constants['Planck constant']

    # Boltzmann constant
    k = scipy.constants.physical_constants['Boltzmann constant']

    # calculation of Planck function
    blackbody = 2.0 * h[0] * c[0]**2 / wavelength**5 \
        / (numpy.exp (h[0] * c[0] / (wavelength * k[0] * T) ) - 1.0 )

    # returning blackbody curve
    return (blackbody)

# making objects "fig", "canvas", and "ax"
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111)
    
# labels
ax.set_xlabel ('Wavelength [$\mu$m]')
ax.set_ylabel ('Specific Intensity [W sr$^{-1}$ m$^{-3}$]')

# showing UV region
ax.fill_between ([0.03, 0.3], 10**-2, 10**18, color='violet', alpha=0.2)
ax.text (x=0.07, y=10**1, s='UV')

# showing visible region
ax.fill_between ([0.3, 1.0], 10**-2, 10**18, color='green', alpha=0.1)
ax.text (x=0.35, y=10**1, s='Visible')

# showing IR region
ax.fill_between ([1.0, 1000.0], 10**-2, 10**18, color='red', alpha=0.1)
ax.text (x=10.0, y=10**1, s='IR')

# range of X-axis and Y-axis
x_min = 0.03
x_max = 1000.0
y_min = 1.0
y_max = 0.0

# calculations
for T in list_temperature:
    # printing temperature of blackbody
    print (f'Temperature:')
    print (f'  T = {T} K')

    # range of wavelength (from 10**-8 m = 10 nm to 10**-3 m = 1 mm)
    wavelength_min = -8.0
    wavelength_max = -3.0

    # wavelength in metre
    wavelength = numpy.logspace (wavelength_min, wavelength_max, num=5001)

    # blackbody spectrum
    bb_spectrum = bb_lambda (wavelength, T)

    # maximum value of flux
    if (y_max < bb_spectrum.max () * 3.0):
        y_max = bb_spectrum.max () * 3.0

    # printing Planck function
    print (f'Wavelength:')
    print (f'{wavelength}')
    print (f'Planck function:')
    print (f'{bb_spectrum}')

    # plotting data
    ax.plot (wavelength * 10**6, bb_spectrum, \
             linewidth=3, label=f'Blackbody of T = {T} K')

# axes
ax.set_xscale ('log')
ax.set_yscale ('log')
ax.set_xlim (0.03, 1000.0)
ax.set_ylim (10**0, bb_spectrum.max () * 3)

# making legend
ax.legend ()

# saving the plot into a file
fig.savefig (file_output, dpi=225)
