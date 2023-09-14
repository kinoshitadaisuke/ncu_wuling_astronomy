#!/usr/pkg/bin/python3.10

#
# Time-stamp: <2023/09/14 12:12:06 (CST) daisuke>
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
def bb_nu (frequency, T):
    # speed of light
    c = scipy.constants.physical_constants['speed of light in vacuum']

    # Planck constant
    h = scipy.constants.physical_constants['Planck constant']

    # Boltzmann constant
    k = scipy.constants.physical_constants['Boltzmann constant']

    # calculation of Planck function
    blackbody = 2.0 * h[0] * frequency**3 / c[0]**2 \
        / (numpy.exp (h[0] * frequency / (k[0] * T) ) - 1.0 )

    # returning blackbody curve
    return (blackbody)

# range of frequency (from 10**0 Hz to 10**16 Hz)
frequency_min = 2.0
frequency_max = 20.0

# frequency in Hz
frequency = numpy.logspace (frequency_min, frequency_max, num=16001, \
                            dtype=numpy.longdouble)

# making objects "fig", "canvas", and "ax"
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111)

# labels
ax.set_xlabel ('Frequency [Hz]')
ax.set_ylabel ('Specific Intensity [W sr$^{-1}$ m$^{-2}$ Hz$^{-1}$]')

# axes
ax.set_xscale ('log')
ax.set_yscale ('log')
ax.set_xlim (10**3, 10**19)
ax.set_ylim (10**-30, 10**6)

# make secondary X-axis
c   = scipy.constants.physical_constants['speed of light in vacuum'][0]
ax2 = ax.secondary_xaxis (location='top', \
                          functions=(lambda x: c/x, lambda x: c/x) )
ax2.set_xlabel ('Wavelength [m]')

# showing X-ray region
ax.fill_between (numpy.array ([3*10**16, 3*10**19], dtype=numpy.longdouble), \
                 10**-30, 10**8, \
                 color='cyan', alpha=0.1)
ax.text (x=3*10**17, y=10**-29, s='X-ray')

# showing UV region
ax.fill_between ([10**15, 3*10**16], 10**-30, 10**8, \
                 color='violet', alpha=0.2)
ax.text (x=2*10**15, y=10**-29, s='UV')

# showing visible region
ax.fill_between ([3*10**14, 10**15], 10**-30, 10**8, \
                 color='green', alpha=0.1)
ax.text (x=10**14, y=3*10**-28, s='Visible')

# showing IR region
ax.fill_between ([10**12, 3*10**14], 10**-30, 10**8, \
                 color='red', alpha=0.1)
ax.text (x=10**13, y=10**-29, s='IR')

# showing radio region
ax.fill_between ([10**0, 10**12], 10**-30, 10**8, \
                 color='yellow', alpha=0.1)
ax.text (x=10**8, y=10**-29, s='Radio')

# calculations
for T in list_temperature:
    # printing temperature of blackbody
    print (f'Temperature:')
    print (f'  T = {T} K')

    # plotting data
    # making model spectrum for given temperature using Planck's radiation law
    bb = bb_nu (frequency, T)

    # label
    text_label = f'T = {T:g} K'
    ax.plot (frequency, bb, linestyle='-', linewidth=3, label=text_label)

# legend
ax.legend (loc='upper left')

# saving the plot into a file
fig.savefig (file_output, dpi=225)
