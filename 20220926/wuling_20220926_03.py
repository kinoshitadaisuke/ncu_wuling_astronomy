#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/09/26 00:48:44 (CST) daisuke>
#

# importing astropy module
import astropy
import astropy.coordinates
import astropy.time
import astropy.units

# importing matplotlib module
import matplotlib.pyplot

# units
u_hr = astropy.units.hour
u_km = astropy.units.km

# setting for solar system ephemeris
astropy.coordinates.solar_system_ephemeris.set ('jpl')

# time t = 2022-10-10T12:00:00 (UTC)
t = astropy.time.Time ('2022-10-10T12:00:00', format='isot', scale='utc')


# getting positions of Sun, Earth, and Moon
earth = astropy.coordinates.get_body_barycentric ('earth', t)
moon  = astropy.coordinates.get_body_barycentric ('moon', t)

# calculation of position of the Moon relative to the Earth
moon_rel_x = (moon.x - earth.x) / u_km
moon_rel_y = (moon.y - earth.y) / u_km

# printing positions of Earth and Moon
print (f'Positions of the Earth and the Moon at t = {t}')
print (f'  Earth : {earth}')
print (f'  Moon  : {moon}')

print (f'')

print (f'Positions of the Moon relative to the Earth at X-Y plane')
print (f'  Moon  : ({moon_rel_x}, {moon_rel_y})')

# making a fig object using matplot.pyplot.figure function
fig = matplotlib.pyplot.figure ()
    
# making an axes object using object-oriented interface
ax = fig.add_subplot (111)

# settings for plot
ax.set_aspect ('equal')
ax.set_xlim (-4.7*10**5, +4.7*10**5)
ax.set_ylim (-4.7*10**5, +4.7*10**5)
ax.set_xlabel ("X [km]")
ax.set_ylabel ("Y [km]")
ax.set_title ("Position of the Moon relative to the Earth")

# plotting the Earth
ax.plot (0.0, 0.0, marker='o', markersize=25, color='blue', label='Earth')
ax.text (0.0, -8.0*10**4, f'Earth')

# plotting the Moon
ax.plot (moon_rel_x, moon_rel_y, marker='o', markersize=15, \
         color='orange', label='Moon')
ax.text (moon_rel_x, moon_rel_y - 8.0*10**4, f'Moon')

# plotting the time
ax.text (-4.55*10**5, -4.55*10**5, f'Date/Time: {t} (UTC)')

# grid
ax.grid ()

# showing plot
matplotlib.pyplot.show ()
