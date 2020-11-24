from tabletop_connector_api.events.utils import address_to_geocode


def test_valid_address():
    valid_dict = {
        "country": "Poland",
        "city": "Gdansk",
        "street": "Wita Stwosza",
        "postal_code": "80-306",
        "number": "57"
    }

    assert address_to_geocode(valid_dict) == (54.395704550000005, 18.5739726651911)


def test_invalid_address():
    valid_dict = {
        "country": "xD",
        "city": "xD",
        "street": "xD",
        "postal_code": "21-037",
        "number": "222"
    }

    assert address_to_geocode(valid_dict) == ()
