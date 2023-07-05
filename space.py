from skyfield.api import load

# Create a timescale and ask the current time.
ts = load.timescale()
t = ts.now()

breakpoint()
# Load the JPL ephemeris DE421 (covers 1900-2050).
planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']

# What's the position of Mars, viewed from Earth?
astrometric = earth.at(t).observe(mars)
ra, dec, distance = astrometric.radec()

print(ra)
print(dec)
print(distance)

## Example 2
print("--------- Example 2 -------------")

from skyfield.api import N, W, wgs84

boston = earth + wgs84.latlon(42.3583 * N, 71.0636 * W)
astrometric = boston.at(t).observe(mars)
alt, az, d = astrometric.apparent().altaz()

print(alt)
print(az)

print("--------- Attempt 1 -------------")

astrometric = boston.at(t).observe(planets['sun'])
alt, az, d = astrometric.apparent().altaz()

print(alt)
print(az)

chicago = earth + wgs84.latlon(41.8781 * N, 87.6298 * W)
astrometric = chicago.at(t).observe(planets['sun'])
alt, az, d = astrometric.apparent().altaz()

print(alt)
print(az)


