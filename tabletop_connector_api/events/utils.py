import math

from geopy.geocoders import Nominatim


def address_to_geocode(address: dict):

    result = Nominatim(user_agent="xd").geocode(address.get("country") + " "
                               + address.get("city") + " "
                               + address.get("postal_code") + " "
                               + address.get("street") + " "
                               + address.get("number"))

    try:
        return result.latitude, result.longitude
    except AttributeError:
        return ()


def get_distance_in_kilometers(from_lat, from_long, to_lat, to_long):
    R = 6371e3
    pi = math.pi
    x1 = from_lat * pi/180
    x2 = to_lat * pi/180
    delta1 = (to_lat-from_lat) * pi/180
    delta2 = (to_long-from_long) * pi/180
    a = math.sin(delta1/2)**2 + math.cos(x1) * math.cos(x2) * math.sin(delta2/2)**2
    c = 2 * math.atan2(a**0.5, (1-a)**0.5)

    return R * c / 1000

