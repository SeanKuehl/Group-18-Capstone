from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    #the username and email are already handled from base user and username can double as account name, so this is it
    account_bio = models.TextField()
    reported_count = models.PositiveIntegerField(default=0)
    admin_status = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    steam_id = models.CharField(max_length=20, blank=True, null=True)
    steam_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


