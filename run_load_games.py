import django
django.setup()
from tabletop_connector_api.events.utils import load_games


load_games()