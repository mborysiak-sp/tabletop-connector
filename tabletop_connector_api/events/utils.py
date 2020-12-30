import math
import os
import pandas as pd
from geopy import Here
from geopy.adapters import AdapterHTTPError
from geopy.exc import GeocoderQueryError

from tabletop_connector_api.events.models import Game


def geocode_to_address(geocode: tuple):
    def parse_address(address_dict):
        address_dict = {
            'number': address_dict['HouseNumber'],
            'street': address_dict.get('Street'),
            'city': address_dict.get('City'),
            'postal_code': address_dict['PostalCode'],
            'country': address_dict['AdditionalData'][0]['value']
        }
        return address_dict

    try:
        address = Here(apikey=os.getenv('HERE_APIKEY')).reverse(geocode)
        address_components = address.raw['Location']['Address']
        parsed_address = parse_address(address_components)
        return parsed_address
    except AttributeError:
        return ()
    except TypeError:
        return ()
    except ValueError:
        return ()


def address_to_geocode(address: dict):
    query = address.get("country", "") + " " \
            + address.get("city", "") + " " \
            + address.get("postal_code", "") + " " \
            + address.get("street", "") + " " \
            + address.get("number", "")
    try:
        result = Here(apikey=os.getenv('HERE_APIKEY')).geocode(query)
        return result.latitude, result.longitude
    except AttributeError:
        return ()
    except IndexError:
        return ()
    except GeocoderQueryError:
        return ()


def get_distance_in_kilometers(from_lat, from_long, to_lat, to_long):
    R = 6371e3
    pi = math.pi
    x1 = from_lat * pi / 180
    x2 = to_lat * pi / 180
    delta1 = (to_lat - from_lat) * pi / 180
    delta2 = (to_long - from_long) * pi / 180
    a = math.sin(delta1 / 2) ** 2 + math.cos(x1) * math.cos(x2) * math.sin(delta2 / 2) ** 2
    c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)

    return R * c / 1000


def load_games():
    """This function loads database exported from BGG into the project"""
    if not Game.objects.exists():
        try:
            print('Trying to load games games...')
            df = pd.read_csv(os.path.join('data', 'games.csv'))
        except FileNotFoundError:
            print('File not found')
        df.dropna(inplace=True)
        row_iter = df.iterrows()
        games = [
            Game(name=row['name'],
                 image=row['image'],
                 thumbnail=row['thumbnail'],
                 min_players=row['min_players'],
                 max_players=row['max_players'],
                 playtime=row['play_time'])
            for index, row in row_iter
        ]
        Game.objects.bulk_create(games)
        print('Games loaded')
