#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/13 03:34:31 (CST) daisuke>
#

# importing numpy module
import numpy

# importing astropy module
import astropy
import astropy.coordinates
import astropy.time
import astropy.units

# importing matplotlib module
import matplotlib.animation
import matplotlib.backends.backend_agg
import matplotlib.figure

# output file name
file_output = 'wuling_20230313_05.mp4'

# units
u_hr = astropy.units.hour
u_km = astropy.units.km

# setting for solar system ephemeris
astropy.coordinates.solar_system_ephemeris.set ('jpl')

# time to start the simulation: t0 = 2023-01-01T00:00:00 (UTC)
t0 = astropy.time.Time ('2023-01-01T00:00:00', format='isot', scale='utc')

# number of steps (total length of animation = (n / 24) days
n = 4320

# making an empty list for animation
frames = []

# making a fig object
fig = matplotlib.figure.Figure ()

# making a canvas object
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)

# making an axes object
ax = fig.add_subplot (111)

for i in range (n):
    # time t
    t = t0 + i * u_hr

    # getting positions of Earth and Moon
    earth = astropy.coordinates.get_body_barycentric ('earth', t)
    moon  = astropy.coordinates.get_body_barycentric ('moon', t)

    # calculation of position of the Moon relative to the Earth
    moon_rel_x = (moon.x - earth.x) / u_km
    moon_rel_y = (moon.y - earth.y) / u_km

    # settings for plot
    ax.set_aspect ('equal')
    ax.set_xlim (-4.7*10**5, +4.7*10**5)
    ax.set_ylim (-4.7*10**5, +4.7*10**5)
    ax.set_xlabel ("X [km]")
    ax.set_ylabel ("Y [km]")
    ax.set_title ("Position of the Moon relative to the Earth")
    
    # list of objects to plot
    list_obj = []
    
    # plotting the Earth
    earth, = ax.plot (0.0, 0.0, marker='o', markersize=25, \
                      color='blue', label='Earth')
    list_obj.append (earth)
    text_earth = ax.text (0.0, -8.0*10**4, f'Earth')
    list_obj.append (text_earth)

    # plotting the Moon
    moon,  = ax.plot (moon_rel_x, moon_rel_y, marker='o', markersize=15, \
                      color='orange', label='Moon')
    list_obj.append (moon)
    text_moon = ax.text (moon_rel_x, moon_rel_y - 8.0*10**4, f'Moon')
    list_obj.append (text_moon)

    # plotting the time
    text_time  = ax.text (-4.55*10**5, -4.55*10**5, f'Date/Time: {t} (UTC)')
    list_obj.append (text_time)

    # plotting grid
    grid_x = numpy.linspace (-4.0*10**5, +4.0*10**5, 9)
    grid_y = numpy.linspace (-4.0*10**5, +4.0*10**5, 9)
    for x in grid_x:
        grid, = ax.plot ([x, x], [-1.0*10**7, +1.0*10**7], \
                         linestyle='--', color='gray', alpha=0.3)
        list_obj.append (grid)
    for y in grid_y:
        grid, = ax.plot ([-1.0*10**7, +1.0*10**7], [y, y], \
                         linestyle='--', color='gray', alpha=0.3)
        list_obj.append (grid)

    # appending the plot to animation
    frames.append (list_obj)

# making animation
anim = matplotlib.animation.ArtistAnimation (fig, frames, interval=50)

# saving file
anim.save (file_output, dpi=225)
