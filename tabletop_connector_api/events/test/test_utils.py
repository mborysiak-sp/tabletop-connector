from tabletop_connector_api.events.utils import address_to_geocode


class Geocode_test:

    def test_valid_address(self):
        valid_dict = {
            "country": "Poland",
            "city": "Gdansk",
            "street": "Wita Stwosza",
            "postal_code": "80-306",
            "number": "57"
        }

        assert address_to_geocode(valid_dict) is None

    def test_invalid_address(self):
        pass