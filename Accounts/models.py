from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    #the username and email are already handled from base user and username can double as account name, so this is it
    account_bio = models.TextField()
    reported_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username


