from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from . import signals
        signals.post_save.connect(signals.create_friendship, sender=self.get_model('User'))