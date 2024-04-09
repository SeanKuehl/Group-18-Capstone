from Main.models import Account
from django.db import models

# Identify duplicate usernames
duplicate_usernames = Account.objects.values('username').annotate(count=models.Count('username')).filter(count__gt=1)

# Assuming you want to keep only one instance of each duplicate username
for username in duplicate_usernames:
    # Get all instances of the duplicate username
    duplicate_accounts = Account.objects.filter(username=username['username'])
    
    # Keep the first instance and delete the rest
    for account in duplicate_accounts[1:]:
        account.delete()