import math
import os
import pandas as pd
from geopy.geocoders import Nominatim
from tabletop_connector_api.events.models import Game


def geocode_to_address(geocode: tuple):
    def parse_address(address_string :str):
        # works only for poland and polish towns
        address_list = address_string.split(', ')
        address_dict = {
            'number': address_list[0],
            'street': address_list[1],
            'city': address_list[3],
            'postal_code': address_list[-2],
            'country': address_list[-1]
        }
        return address_dict

    try:
        address = Nominatim(user_agent="xd").reverse(geocode)
        return parse_address(address.address)
    except AttributeError:
        return ()
    except TypeError:
        return ()


def address_to_geocode(address: dict):
    try:
        result = Nominatim(user_agent="xd").geocode(address.get("country", [""])[0] + " "
                                                    + address.get("city", [""])[0] + " "
                                                    # + address.get("postal_code", "") + " "
                                                    + address.get("street", [""])[0] + " "
                                                    + address.get("number", [""])[0])
        try:
            return result.latitude, result.longitude
        except AttributeError:
            return ()

    except IndexError:
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
