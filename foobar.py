import ephem
import datetime
import math

import pytz

from math import atan, sqrt
from math import atan2, cos, sin, radians
from haversine import haversine, Unit

def bearing(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate the bearing angle
    y = sin(lon2 - lon1) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1)
    bearing_angle = atan2(y, x)

    # Convert bearing angle to degrees and normalize to 0-360 range
    bearing_angle = (bearing_angle * 180 / math.pi + 360) % 360

    return bearing_angle

def vertical_angle(lat1, lon1, elev1, lat2, lon2, elev2):
    # Calculate the distance between the two points
    distance = haversine((lat1, lon1), (lat2, lon2), unit=Unit.METERS) #/ 1000
    print(distance)
    # Calculate the vertical distance between the two points
    vertical_distance = elev2 - elev1

    # Calculate the vertical angle
    vertical_angle = atan(vertical_distance / distance)

    # Convert vertical angle to degrees
    vertical_angle = vertical_angle * 180 / math.pi

    return vertical_angle

#lat1, lon1, elev1 = 37.7749, -122.4194, 1000
#lat2, lon2, elev2 = 40.7128, -74.0060, 0

class Position:
    """lat, lon, elevation -> observer
    """
    def __init__(self, lat=None, lon=None, elevation=None):
        self.lat = lat
        self.lon = lon
        self.elevation = elevation
    
    def get_observer(self):
        "return ephem.Observer object"
        
        observer = ephem.Observer()
        observer.lon = self.lon  # Longitude of observer (in degrees West)
        observer.lat = self.lat  # Latitude of observer (in degrees North)
        observer.elevation = self.elevation # Elevation of observer (in meters)

        return observer


def calc_sun_pos(observer: ephem.Observer, dt: datetime.datetime):
        
    # Set date and time (in UTC)
    dt_str = (dt).strftime("%Y/%m/%d %H:%M:%S") 
    observer.date = dt_str #'2023/04/13 23:00:00'  # Date and time
    sun = ephem.Sun(observer)
    sun.compute(observer)

    
    sun_altitude, sun_azimuth = math.degrees(sun.alt), math.degrees(sun.az)

    return sun_altitude, sun_azimuth

#obs_chi = Position(lat='-87.6298', lon='41.8781', elevation=180).get_observer()
pos_test = Position(lat='41.8812875', lon='-87.6351478', elevation=180)

# 1 foot = 0.3048 meters
obs_searstower = Position(lat='41.8790723', lon='-87.6358972', elevation=(1450 + 1729) / 2 * 0.3048) # base 1,450′, 1,729′ to tip


bearing_angle = bearing(
    float(pos_test.lat), float(pos_test.lon),
    float(obs_searstower.lat), float(obs_searstower.lon))
vertical_angle = vertical_angle(
    float(pos_test.lat), float(pos_test.lon), pos_test.elevation,
    float(obs_searstower.lat), float(obs_searstower.lon), obs_searstower.elevation)

print("Heading angle:", bearing_angle)
print("Vertical angle:", vertical_angle)

print("----- Find sun pos at times ------")

def date_range_complex(start_date, end_date, days=1, hours=0, hour_limit=None):
    """
    hour_limit: optional, pair of ints to limit start/end time to include in range
    """

    if hour_limit is None:
        hour_limit = [0,24]

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    current_date = start_date
    while current_date < end_date:
        hour_iter = hour_limit[0]
        while hour_iter < hour_limit[-1] and hours > 0:
            yield current_date
            #if current_date.hour >= hour_limit[0]:
            current_date += datetime.timedelta(hours=hour_iter)
            #hours_iter = 
        current_date += datetime.timedelta(days=days)

def date_range(start_date, end_date, days=1, hours=0):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    current_date = start_date
    while current_date < end_date:
        yield current_date
        current_date += datetime.timedelta(hours=hours)

start_date = '2023-03-01 12:00:00'
end_date = '2023-06-30 12:00:00'
days_increment = 1
hours_increment = 1/60.

date_generator = [x for x in date_range(start_date, end_date, days=days_increment, hours=hours_increment) if (x.hour >= 11 and x.hour <= 14)] 

obs_test = pos_test.get_observer()



target_altitude, target_azimuth = vertical_angle, bearing_angle
min_error = 100000000
min_time = None
min_coords = None

for date in date_generator:
    #dt_local = datetime.datetime(2023, 6, 21, 12, tzinfo=pytz.timezone('US/Central'))

    dt = date.replace(tzinfo=pytz.timezone('US/Central'))
    dt_utc = dt.astimezone(pytz.UTC)
    sun_altitude, sun_azimuth = calc_sun_pos(obs_test, dt_utc)

    squared_error = math.sqrt((target_altitude - sun_altitude) ** 2 + (target_azimuth - sun_azimuth) ** 2)
    if squared_error < min_error:
        min_error = squared_error
        min_coords = (sun_altitude, sun_azimuth, date)


print(min_error, min_coords)

    #print(f"Sun position (Altitude, Compass): ({sun_altitude}, {sun_azimuth}) at {dt}")



dt_local = datetime.datetime(2023, 6, 21, 12, tzinfo=pytz.timezone('US/Central'))


#sun_altitude, sun_azimuth = calc_sun_pos(obs_chi, dt_local.astimezone(pytz.UTC))

# Print the position of the sun in compass coordinates
print(f"Sun position (Altitude, Compass): ({sun_altitude}, {sun_azimuth})")

# TODO make datetime with tz aware code
# TODO add methods to compare relative positions of two points
# TODO for loop to find when sun is closest to a target pair of angles
# TODO Franklin street calc

#obs = ephem.Observer()
#obs.lon = '-87.6298'  # Longitude of observer (in degrees West)
#obs.lat = '41.8781'  # Latitude of observer (in degrees North)
#obs.elevation = 180  # Elevation of observer (in meters)

# Set date and time (in UTC)
#dt_str = (datetime.datetime.utcnow() - datetime.timedelta(hours=2)).strftime("%Y/%m/%d %H:%M:%S") 
#print(dt_str)
#obs.date = dt_str #'2023/04/13 23:00:00'  # Date and time

# Calculate position of the sun
# Set the observer's location (latitude, longitude, elevation in meters)
#observer = ephem.Observer()
#observer.lat = '51.5074'  # London's latitude
#observer.lon = '0.1278'  # London's longitude
#observer.elevation = 10   # London's elevation in meters

# Set the date and time of interest
#obs.date = '2021/11/01 17:00:00'  # YYYY/MM/DD HH:MM:SS in UTC

# Iterate over time and get suns position