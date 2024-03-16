from django.db import models

# Create your models here.


class Account(models.Model):
    #username and email are here to tie object back to user model for later
    
    username = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    account_name = models.CharField(max_length=128)
    account_bio = models.TextField()

class Tag(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Post(models.Model):

    #username and email are here to tie object back to user model for later
    username = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    post_title = models.CharField(max_length=128)
    post_community = models.CharField(max_length=128)
    post_body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField("Tag", related_name="posts")

    """
    post_tags = models.CharField(
        max_length=50,
        choices=game_choices,
        default="COD",
    )
    """

    def __str__(self):
        return self.post_title

    """
    game_choices = {
        ("COD", "Call Of Duty"),
        ("MTG", "Magic The Gathering"),
        ("HD", "Hell Divers"),
        ("RF", "Risk Factions"),
        ("C", "Chess"),
    }
    """

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"