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
