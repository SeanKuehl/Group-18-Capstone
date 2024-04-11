from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    #username and email are here to tie object back to user model for later
    
    username = models.CharField(max_length=128, null=True, unique=True)
    password = models.CharField(max_length=64, default = 'password')
    email = models.CharField(max_length=128)
    account_name = models.CharField(max_length=128)
    account_bio = models.TextField()
    reported_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


#yes this stuff is crazy, I got it from here for reference: https://simpleisbetterthancomplex.com/tutorial/2016/10/13/how-to-use-generic-relations.html
class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Post(models.Model):
    accountname = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    post_title = models.CharField(max_length=128)
    post_community = models.CharField(max_length=128)
    post_body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField("Tag", related_name="posts")
    votes = GenericRelation(Activity)
    reported_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.post_title

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"
    



