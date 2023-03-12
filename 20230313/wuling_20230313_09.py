#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/13 04:26:08 (CST) daisuke>
#

# importing numpy module
import numpy

# importing astropy module
import astropy.coordinates
import astropy.time
import astropy.units

# importing astroplan module
import astroplan

# units
u_m   = astropy.units.m
u_deg = astropy.units.degree
u_hr  = astropy.units.hour

# using "DE440" for solar system ephemeris
astropy.coordinates.solar_system_ephemeris.set ('de440')

# location of observer: Wuling High School (coordinates from Google Maps)
longitude = 121.28571012626854 * u_deg
latitude  = 24.9877016296871 * u_deg
height    = 100.0 * u_m

# making a location object using Astropy
location = astropy.coordinates.EarthLocation.from_geodetic (lon=longitude, \
                                                            lat=latitude, \
                                                            height=height)

# making an observer object
observer = astroplan.Observer (location=location, name='NCU', \
                               timezone='Asia/Taipei')

# timezone in Taiwan
tz_taiwan = astropy.time.TimezoneInfo (utc_offset=8.0 * u_hr)

# initial guess time
try:
    YYYY = int (input ('Year: '))
except:
    print (f'Type an integer for Year.')
    sys.exit (1)
try:
    MM   = int (input ('Month: '))
except:
    print (f'Type an integer for Month.')
    sys.exit (1)
try:
    DD   = int (input ('Day: '))
except:
    print (f'Type an integer for Day.')
    sys.exit (1)

# date/time
initial_guess_str = f'{YYYY:04d}-{MM:02d}-{DD:02d} 16:00:00'
time = astropy.time.Time (initial_guess_str, format='iso', scale='utc')

# moon rise time
moonrise = observer.moon_rise_time (time, which='nearest', \
                                    n_grid_points=500)

# moon set time
moonset = observer.moon_set_time (time, which='nearest', \
                                  n_grid_points=500)

# printing location
print (f'Location:')
print (f'  longitude = {location.lon:8.4f}')
print (f'  latitude  = {location.lat:8.4f}')
print (f'  altitude  = {location.height:8.4f}')

# printing result
print (f'Moon rise and set time:')
print (f'  moon rise time = {moonrise.to_datetime (timezone=tz_taiwan)}')
print (f'  moon set time  = {moonset.to_datetime (timezone=tz_taiwan)}')
