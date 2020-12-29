from tabletop_connector_api.events.utils import (
    address_to_geocode,
    get_distance_in_kilometers,
    geocode_to_address,
)


def test_valid_address():
    valid_dict = {
        "country": ["Poland"],
        "city": ["Gdynia"],
        "street": ["2 morskiego pulku strzelcow"],
        "postal_code": ["81-661"],
        "number": ["6"],
    }

    assert address_to_geocode(valid_dict) == (54.491011150000006, 18.511290835245834)


def test_valid_address_shortened():
    valid_dict = {"city": ["Gdansk"], "street": ["Wita Stwosza"], "number": ["57"]}

    assert address_to_geocode(valid_dict) == (54.395704550000005, 18.5739726651911)


def test_invalid_address():
    valid_dict = {
        "country": [""],
        "city": [""],
        "street": [""],
        "postal_code": [""],
        "number": [""],
    }

    assert address_to_geocode(valid_dict) == ()


def test_get_distance_in_kilometers_with_zeros():

    assert get_distance_in_kilometers(0, 0, 0, 0) == 0


def test_get_distance_in_kilometers_same_sign():
    assert abs(get_distance_in_kilometers(10, 10, 20, 20) - 1544.68) < 0.1


def test_get_distance_in_kilometers_different_sign():
    assert abs(get_distance_in_kilometers(-10, 10, 10, -10) - 3137.04) < 0.1


def test_geocode_to_address():
    address = geocode_to_address((54.395704550000005, 18.5739726651911))

    assert address["number"] == "57"
    assert address["city"] == "Gdansk"
    assert address["street"] == "Wita Stwosza"
