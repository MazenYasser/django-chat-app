from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            User.objects.create(
                username="Mazen",
                email="mazenyasser225@gmail.com",
                password="112001",
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
        
        self.stdout.write(self.style.SUCCESS("Superuser created."))
