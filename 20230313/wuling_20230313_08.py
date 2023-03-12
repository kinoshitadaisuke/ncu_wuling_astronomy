#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2023/03/13 04:27:41 (CST) daisuke>
#

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
observer = astroplan.Observer (location=location, name='WulingHighSchool', \
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

# sunrise time
initial_guess_str = f'{YYYY:04d}-{MM:02d}-{DD:02d} 00:00:00'
sunrise_guess = astropy.time.Time (initial_guess_str, \
                                  format='iso', scale='utc')
sunrise = observer.sun_rise_time (sunrise_guess, which='nearest', \
                                  n_grid_points=500)

# getting position of the Sun
sun = astropy.coordinates.get_body ('sun', sunrise, location=location)

# conversion from equatorial into horizontal
altaz     = astropy.coordinates.AltAz (obstime=sunrise, location=location)
sun_altaz = sun.transform_to (altaz)
sun_alt   = sun_altaz.alt
sun_az    = sun_altaz.az

# printing created observer object
print (f'Location:')
print (f'  longitude = {location.lon:8.4f}')
print (f'  latitude  = {location.lat:8.4f}')
print (f'  altitude  = {location.height:8.4f}')

# printing sunrise time
print (f'Initial guess:')
print (f'  JD                   = {sunrise_guess.jd}')
print (f'  UT                   = {sunrise_guess.iso}')
print (f'  local time in Taiwan = {sunrise_guess.to_datetime (timezone=tz_taiwan)}')
print (f'Sunrise time:')
print (f'  JD                   = {sunrise.jd}')
print (f'  UT                   = {sunrise.iso}')
print (f'  local time in Taiwan = {sunrise.to_datetime (timezone=tz_taiwan)}')

# printing altitude and azimuth
print (f'position of the Sun at sunrise:')
print (f'  alt = {sun_alt:8.4f}')
print (f'  az  = {sun_az:8.4f}')
