from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        """ Connect signals in users.signals. """
        import users.signals