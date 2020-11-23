from geopy.geocoders import Nominatim


def address_to_geocode(address: dict):

    return Nominatim().geocode(address.get("country") + " "
                               + address.get("city") + " "
                               + address.get("postal_code") + " "
                               + address.get("street") + " "
                               + address.get("number"))
