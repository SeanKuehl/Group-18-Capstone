from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from Accounts.models import CustomUser

# Create your models here.



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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Post(models.Model):
    #accountname changes to account which is now the user object
    accountname = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
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
    
# Gaming leagues 
class League(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, related_name='owned_leagues', on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='leagues', through='LeagueMembership')
    team_league = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class LeagueMembership(models.Model):
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    # Ensures that a player can join a league only once
    class Meta:
        unique_together = ('player', 'league')

class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(CustomUser, related_name='teams')

    def __str__(self):
        return self.name

class Match(models.Model):
    league = models.ForeignKey(League, related_name='matches', on_delete=models.CASCADE)
    date = models.DateTimeField()
    team1 = models.ForeignKey(Team, related_name='matches_as_team1', on_delete=models.CASCADE, null=True, blank=True)
    team2 = models.ForeignKey(Team, related_name='matches_as_team2', on_delete=models.CASCADE, null=True, blank=True)
    player1 = models.ForeignKey(CustomUser, related_name='matches_as_player1', on_delete=models.CASCADE, null=True, blank=True)
    player2 = models.ForeignKey(CustomUser, related_name='matches_as_player2', on_delete=models.CASCADE, null=True, blank=True)
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)
    player1_score = models.IntegerField(null=True, blank=True)
    player2_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.league.team_league:
            return f"{self.team1} vs {self.team2}"
        else:
            return f"{self.player1} vs {self.player2}"

class UserReview(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    user_reviewed = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.user_reviewed.username}'"
    



class RegisteredBusiness(models.Model):
    business_number = models.IntegerField()
    associated_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)




class DiscountOffer(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    associated_business = models.ForeignKey(RegisteredBusiness, on_delete=models.CASCADE)



class EventPost(models.Model):

    OPEN = "O"
    REGISTRATION_CLOSED = "RC"
    EVENT_CLOSED = "EC"
    
    event_status_choices = {
        ("O", "Open to Registration"),
        ("RC", "Closed to Registration"),
        ("EC", "Event has been Closed"),
        
    }


    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=128)
    post_location = models.CharField(max_length=128)
    post_date_and_time = models.CharField(max_length=128)
    post_body = models.TextField()

    
    event_status = models.CharField(
        max_length=2,
        choices=event_status_choices,
        default=OPEN,
    )

    attendees = models.ManyToManyField(CustomUser, related_name='event', through='EventAttendance')



class EventAttendance(models.Model):
    attendant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(EventPost, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)


    # Ensures that a player can join a event only once
    class Meta:
        unique_together = ('attendant', 'event')

    
    




