from django.db import models

# Create your models here.


class Account(models.Model):
    #username and email are here to tie object back to user model for later
    
    username = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    account_name = models.CharField(max_length=128)
    account_bio = models.TextField()



    



class Post(models.Model):

    
    game_choices = {
        ("COD", "Call Of Duty"),
        ("MTG", "Magic The Gathering"),
        ("HD", "Hell Divers"),
        ("RF", "Risk Factions"),
        ("C", "Chess"),
    }


    #username and email are here to tie object back to user model for later
    username = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    post_title = models.CharField(max_length=128)
    post_community = models.CharField(max_length=128)
    post_body = models.TextField()
    post_tags = models.CharField(
        max_length=50,
        choices=game_choices,
        default="COD",
    )
