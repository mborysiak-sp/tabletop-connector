from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'tabletop_connector_api.users'

    def ready(self):
        import tabletop_connector_api.users.signals
