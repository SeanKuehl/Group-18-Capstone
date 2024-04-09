from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Count

class Command(BaseCommand):
    help = 'Check for duplicate usernames in the Account model'

    def handle(self, *args, **kwargs):
        # Fetch the Account model dynamically
        Account = apps.get_model('Main', 'Account')

        # Check for duplicate usernames
        duplicate_usernames = Account.objects.values('username').annotate(count=Count('username')).filter(count__gt=1)

        # Print any duplicate usernames found
        for item in duplicate_usernames:
            self.stdout.write(self.style.WARNING(f"Duplicate username: {item['username']}"))
