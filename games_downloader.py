"""Games downloader using BGG API"""
import os
import time
import pandas as pd
import requests
import xmltodict
from pyexpat import ExpatError


def extract_game_data(game_dict_raw):
    game_dict = {'id': game_dict_raw['@id'],
                 'image': game_dict_raw.get('image', None),
                 'thumbnail': game_dict_raw.get('thumbnail', None),
                 'name': game_dict_raw['name'][0]['@value'] if type(game_dict_raw['name']) == list
                 else game_dict_raw['name']['@value'],
                 'min_players': game_dict_raw['minplayers']['@value'],
                 'max_players': game_dict_raw['maxplayers']['@value'],
                 'play_time': game_dict_raw['playingtime']['@value'],
                 'min_age': game_dict_raw['minage']['@value']}
    return game_dict


def get_by_name(name):
    game_xml = requests.get(f'https://boardgamegeek.com/xmlapi2/search?query={name}&type=boardgame')
    game_dicts = xmltodict.parse(game_xml.content)
    return game_dicts['items']['item']


def get_by_id(id):
    game_xml = requests.get(f'https://boardgamegeek.com/xmlapi2/thing?id={id}&type=boardgame')
    game_dicts = xmltodict.parse(game_xml.content)
    return game_dicts['items']['item']


def get_in_range(min_value, max_value):
    time.sleep(5)
    ids = ','.join([str(i) for i in range(min_value, max_value)])
    games = []
    while not games:
        try:
            games = get_by_id(ids)
        except ExpatError:
            print('API rejected call, waiting')
            time.sleep(5)
    games_formatted = [extract_game_data(game) for game in games]
    return games_formatted


def scrape_api_data():
    dataframe = pd.DataFrame()

    for i in range(0, 100000, 1000):
        max_range = i + 1000
        games = get_in_range(i, max_range)
        print('got games')
        temp_df = pd.DataFrame(games)
        temp_df.to_pickle(os.path.join('data', 'pickles', f'data{i}.pickle'))
        print('saved pickle')


    dataframe.to_csv(os.path.join('data', 'games.csv'))


if __name__ == '__main__':
    scrape_api_data()
    df = pd.DataFrame()
    if not os.path.join('data', 'games.csv'):
        pickles_folder = os.path.join('data', 'pickles')
        for filename in os.listdir(pickles_folder):
            temp_df = pd.read_pickle(os.path.join(pickles_folder, filename))
            df = df.append(temp_df)
        df.to_csv('games.csv', index=False)