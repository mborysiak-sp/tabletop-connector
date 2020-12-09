import math
import os

import pandas as pd

from geopy.geocoders import Nominatim

from tabletop_connector_api.events.models import Game
from tabletop_connector_api.config.local import BASE_DIR


def address_to_geocode(address: dict):
    result = Nominatim(user_agent="xd").geocode(address.get("country", [""])[0] + " "
                                                + address.get("city", [""])[0] + " "
                                                # + address.get("postal_code", "") + " "
                                                + address.get("street", [""])[0] + " "
                                                + address.get("number", [""])[0])

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


def load_games():
    """This function loads database exported from BGG into the project"""
    print('Loading games...')
    df = pd.read_csv(os.path.join('data', 'games.csv'))
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