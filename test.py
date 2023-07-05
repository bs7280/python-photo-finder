import ephem
import math
import datetime

# Set observer location
obs = ephem.Observer()
obs.lon = '-87.6298'  # Longitude of observer (in degrees West)
obs.lat = '41.8781'  # Latitude of observer (in degrees North)
obs.elevation = 200  # Elevation of observer (in meters)

# Set date and time (in UTC)
dt_str = datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
print(dt_str)
obs.date = dt_str #'2023/04/13 23:00:00'  # Date and time
# Calculate position of the sun
sun = ephem.Sun(obs)
sun.compute(obs)



# Compute the position of the moon
moon = ephem.Moon(obs)
moon.compute(obs)

# Get the moon's right ascension and declination
ra = sun.ra
dec = sun.dec

# Print the moon's position
print('Moon position at', obs.date, 'UTC:')
print('Right ascension:', ra)
print('Declination:', dec)



# Get the position of the sun in equatorial coordinates
sun_ra, sun_dec = sun.ra, sun.dec

# Convert RA and Dec to altitude and azimuth
sun_alt, sun_az = math.degrees(sun.alt), math.degrees(sun.az)

# Convert azimuth to compass coordinates
print(sun_az)
sun_compass = (450 - sun_az) % 360

# Print the position of the sun in compass coordinates
print(f"Sun position (Altitude, Compass): ({sun_alt}, {sun_compass})")