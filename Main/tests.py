from django.http import request
from django.test import Client, RequestFactory, TestCase, client
from django.urls import reverse
from Main.models import *
from Accounts.models import CustomUser
from Main.forms import *

# Create your tests here.

class DiscountTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.client.login(username='jacob', password='top_secret')

        RegisteredBusiness.objects.create(business_number=10296, associated_user=self.user)
        self.obj = RegisteredBusiness.objects.last()

    def test_view_discounts(self):
        request.user = self.user
        response = self.client.get(reverse("discounts"), {'user_id': self.user.id})

        self.assertEqual(response.status_code, 200)

    def test_create_discounts(self):
        request.user = self.user
        response = self.client.post(reverse("discounts"), 
                                    {
                                        "body": "new discount",
                                    },
                                    )
        
        #validate both the route and the model
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DiscountOffer.objects.last().body, "new discount")
        self.assertEqual(DiscountOffer.objects.last().associated_business, self.obj)
        self.assertEqual(DiscountOffer.objects.last().author, self.user.username)


class DiscountTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.client.login(username='jacob', password='top_secret')

        
    def test_register_business_get(self):
        request.user = self.user
        response = self.client.get(reverse("register_business"))
        
        
        self.assertEqual(response.status_code, 200)


    def test_register_business_post(self):
        request.user = self.user
        response = self.client.post(reverse("register_business"), 
                                    {
                                        "business_number": "1007",
                                    },
                                    )
        
        #validate both the route and the model
        self.assertEqual(response.status_code, 302) #302 is a redirection, but in this case the view is supposed to do that
        self.assertEqual(RegisteredBusiness.objects.last().business_number, 1007)
        self.assertEqual(RegisteredBusiness.objects.last().associated_user, self.user)




class EventPostTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.client.login(username='jacob', password='top_secret')

        EventPost.objects.create(author=self.user, post_title="Carmen Sandiego is great", post_location="all over the world", post_date_and_time="all the time", post_body="that's pretty VILE of you")
        self.obj = EventPost.objects.last()

        
    def test_event_post_get(self):
        request.user = self.user
        response = self.client.get(reverse("events"))
        
        
        self.assertEqual(response.status_code, 200)

    def test_event_post_post(self):
        request.user = self.user
        response = self.client.post(reverse("events"), 
                                    {
                                        "post_title": "emo folk metal",
                                        "post_location": "emo folk metal",
                                        "post_date_and_time": "emo folk metal",
                                        "post_body": "emo folk metal",
                                    },
                                    )
        
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(EventPost.objects.last().post_title, "emo folk metal")
        self.assertEqual(EventPost.objects.last().post_location, "emo folk metal")
        self.assertEqual(EventPost.objects.last().post_date_and_time, "emo folk metal")
        self.assertEqual(EventPost.objects.last().post_body, "emo folk metal")

    def test_event_post_this_event_get(self):
        request.user = self.user
        response = self.client.get(reverse("event-detail", kwargs={'event_id':self.obj.id}))
        
        
        self.assertEqual(response.status_code, 200)


    def test_event_post_my_event_get(self):
        request.user = self.user
        response = self.client.get(reverse("my_event", kwargs={'pk':self.obj.id}))
        
        
        self.assertEqual(response.status_code, 200)



    def test_event_post_attend_event_get(self):
        request.user = self.user
        response = self.client.get(reverse("attend", kwargs={'event_id':self.obj.id}))
                                    
        
        
        self.assertEqual(response.status_code, 302)


class AdminTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.user.is_staff = True
        self.user.save()

        self.client.login(username='jacob', password='top_secret')

        EventPost.objects.create(author=self.user, post_title="Carmen Sandiego is great", post_location="all over the world", post_date_and_time="all the time", post_body="that's pretty VILE of you")
        self.obj = EventPost.objects.last()

        CustomUser.objects.create_user(
            username="sorry_sucker", email="hehe@gmail.com", password="owefnowen", account_bio="evil thang",
        )

        self.removable_user = CustomUser.objects.last()

        Post.objects.create(accountname=self.removable_user,post_title="evil", post_community="evil people",
                            post_body="evil stuff")

        self.removable_post = Post.objects.last()


    def test_admin_remove_post(self):
        
        request.user = self.user
        response = self.client.get(reverse("remove_post", kwargs={'pk':self.removable_post.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.last(), None) #there should be no post objects

    def test_admin_remove_user(self):
        request.user = self.user
        response = self.client.get(reverse("remove_accout", kwargs={'pk':self.removable_user.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.last().username, "jacob") #the only user still left should be the super user
    

class PostVoteTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.user.is_staff = True
        self.user.save()

        self.client.login(username='jacob', password='top_secret')

        

        Post.objects.create(accountname=self.user,post_title="evil", post_community="evil people",
                            post_body="evil stuff")

        self.downvote_post = Post.objects.last()


        Post.objects.create(accountname=self.user,post_title="good", post_community="good",
                            post_body="good")

        self.upvote_post = Post.objects.last()


    def test_upvote_on_post(self):
        request.user = self.user
        response = self.client.get(reverse("post_detail", kwargs={'pk':self.upvote_post.id, 'action':1}))    #one is upvote
        

        upvote_we_just_created = Post.objects.get(id=self.upvote_post.id).votes.filter(activity_type=Activity.UP_VOTE, user=request.user).first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(upvote_we_just_created.activity_type, 'U') #just quadruple checking that it's a up vote


    def test_downvote_on_post(self):
        request.user = self.user
        response = self.client.get(reverse("post_detail", kwargs={'pk':self.downvote_post.id, 'action':2}))    #two is downvote
        

        downvote_we_just_created = Post.objects.get(id=self.downvote_post.id).votes.filter(activity_type=Activity.DOWN_VOTE, user=request.user).first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(downvote_we_just_created.activity_type, 'D') #just quadruple checking that it's a down vote


# Test cases for leagues and matches

class CreateLeagueTestCase(TestCase):

    # Set up a user to use for testing
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="TestUser", 
            email="test@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )
        self.client.login(username='TestUser', password='top_secret')


    # Test that user can create a non-team based league 
    def test_create_non_team_league(self):

        request.user = self.user
        form_data = {
            "name": "Test League",
            "description": "This is a test league.",
            "team_league": False, # Indicates as a non-team league
        }
        form = LeagueForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Submit form data to create the league
        response = self.client.post(reverse("create_league"), form_data)
        
        self.assertEqual(response.status_code, 302)                            # Check that the response is a redirect
        created_league = League.objects.get(name="Test League")                # Retrieve created league
        self.assertEqual(created_league.name, "Test League")                   # Check description
        self.assertEqual(created_league.description, "This is a test league.") # Check description
        self.assertFalse(created_league.team_league)                           # Verify league is not team league

    # Test that user can create a team based league 
    def test_create_team_league(self):

        request.user = self.user
        form_data = {
            "name": "Test Team League",
            "description": "This is a test team league.",
            "team_league": True, # Indicates as a team league
        }
        form = LeagueForm(data=form_data)
        self.assertTrue(form.is_valid())

        response = self.client.post(reverse("create_league"), form_data)
        
        self.assertEqual(response.status_code, 302)                                 # Check that the response is a redirect
        created_league = League.objects.get(name="Test Team League")                # Retrieve created league
        self.assertEqual(created_league.name, "Test Team League")                   # Check description
        self.assertEqual(created_league.description, "This is a test team league.") # Check description
        self.assertTrue(created_league.team_league)                                 # Verify league is team league

class ReadLeagueTestCase(TestCase):

    # Set up a user to use for testing
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.user = CustomUser.objects.create_user(
            username="TestUser", 
            email="test@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.client.login(username='TestUser', password='top_secret')

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=False  
        )

    # Test that user can retrieve a specific league
    def test_read_specific_league(self):

        response = self.client.get(reverse("league_detail", kwargs={'league_id': self.league.id}))

        self.assertEqual(response.status_code, 200)                     # Check for successful retrieval
        self.assertContains(response, "Test League")                    # Verify league name
        self.assertContains(response, "This is a test league.")         # Check description
        self.assertTemplateUsed(response, 'leagues/league_detail.html') # Ensure the correct template is being used

   # Test that user can retrieve all leagues
    def test_read_all_leagues(self):

        response = self.client.get(reverse("league_list"))              # Retrieve all leagues on the leagues list page

        self.assertEqual(response.status_code, 200)                    # Check for successful retrieval
        self.assertContains(response, "Test League")                   # Verify league name
        self.assertTemplateUsed(response, 'leagues/league_list.html')  # Ensure the correct template is being used

class UpdateLeagueTestCase(TestCase):

    # Set up for testing
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.user = CustomUser.objects.create_user(
            username="TestUser", 
            email="test@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.user2 = CustomUser.objects.create_user(
            username="TestUser2", 
            email="test2@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=False  
        )

    def test_update_league_success(self):

        self.client.login(username='TestUser', password='top_secret')

        updated_data = {
            'name': 'Updated League Name',
            'description': 'Updated description of the league.'
        }

        form = LeagueForm(data=updated_data)
        self.assertTrue(form.is_valid())
       
        response = self.client.post(reverse('update_league', kwargs={'league_id': self.league.id}), updated_data)
        
        self.assertEqual(response.status_code, 302) # Check for successful redirect
        self.league.refresh_from_db()               # Refresh the league object from the database
        
        # Verify that the league content has been updated
        self.assertEqual(self.league.name, 'Updated League Name') 
        self.assertEqual(self.league.description, 'Updated description of the league.') 

    def test_update_league_fail(self):

        self.client.login(username='TestUser2', password='top_secret') # User is not owner of league
        
        # Prepare updated data
        updated_data = {
            'name': 'Updated League Name',
            'description': 'Updated description of the league.'
        }

        response = self.client.post(reverse('update_league', kwargs={'league_id': self.league.id}), updated_data)
        
        self.assertEqual(response.status_code, 302) # Check for successful redirect
        self.league.refresh_from_db()               # Refresh the league object from the database
        
        # Verify that the league has not been updated
        self.assertEqual(self.league.name, 'Test League')
        self.assertEqual(self.league.description, 'This is a test league.')

class DeleteLeagueTestCase(TestCase):

    # Set up for testing
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.user = CustomUser.objects.create_user(
            username="TestUser", 
            email="test@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.user2 = CustomUser.objects.create_user(
            username="TestUser2", 
            email="test2@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=False  
        )

    # Test that user who owns league can delete the league
    def test_delete_league_success(self):

        self.client.login(username='TestUser', password='top_secret')

        league_to_delete = League.objects.get(name='Test League') # Retrieve the league to be deleted

        response = self.client.delete(reverse('delete_league', kwargs={'league_id': league_to_delete.id}))

        self.assertEqual(response.status_code, 302)  # Check for successful redirect after deletion

        # Verify that the league has been deleted from the database
        with self.assertRaises(League.DoesNotExist):
            League.objects.get(id=league_to_delete.id)

    def test_delete_league_fail(self):

        self.client.login(username='TestUser2', password='top_secret')

        league_to_delete = League.objects.get(name='Test League') # Retrieve the league to be deleted

        response = self.client.delete(reverse('delete_league', kwargs={'league_id': league_to_delete.id}))

        self.assertEqual(response.status_code, 404)               # Check for successful not found 

        # Verify that the league still exists in the database
        self.assertTrue(League.objects.filter(id=league_to_delete.id).exists())

class CreateTeamTestCase(TestCase):

    # Set up for testing
    def setUp(self):

        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username="TestUser", 
            email="test@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.user2 = CustomUser.objects.create_user(
            username="TestUser2", 
            email="test2@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True  # Assuming this is a team league
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)
        LeagueMembership.objects.create(player=self.user2, league=self.league)

    # Test that user can create a team 
    def test_create_team(self):
        self.client.login(username='TestUser', password='top_secret')

        team_data = {
            'name': 'Test Team',
            'members': [self.user.id]  # Assuming user is a member of the league
        }

        response = self.client.post(reverse('create_team', kwargs={'league_id': self.league.id}), team_data)
        
        self.assertEqual(response.status_code, 302)                                         # Check for successful redirect
        self.assertTrue(Team.objects.filter(name='Test Team', league=self.league).exists()) # Verify that team was created

class ReadTeamTestCase(TestCase):

     # Set up for testing
    def setUp(self):

        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username="TestUser", 
            email="test@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.user2 = CustomUser.objects.create_user(
            username="TestUser2", 
            email="test2@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True  # Assuming this is a team league
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)
        LeagueMembership.objects.create(player=self.user2, league=self.league)

    # Test that user can view team details
    def test_view_team_detail(self):
        self.client.login(username='TestUser', password='top_secret')

        team = Team.objects.create(name='Test Team', league=self.league)
        team.members.add(self.user)

        response = self.client.get(reverse('team_detail', kwargs={'league_id': self.league.id, 'team_id': team.id}))

        self.assertEqual(response.status_code, 200)  # Check for successful response
        self.assertContains(response, 'Test Team')   # Check if team name is in response content

class UpdateTeamTestCase(TestCase):

    # Set up for testing
    def setUp(self):

        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username="TestUser", 
            email="test@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.user2 = CustomUser.objects.create_user(
            username="TestUser2", 
            email="test2@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True  # Assuming this is a team league
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)
        LeagueMembership.objects.create(player=self.user2, league=self.league)

    # Test that user can update team details
    def test_update_team(self):
        self.client.login(username='TestUser', password='top_secret')

        team = Team.objects.create(name='Test Team', league=self.league)
        team.members.add(self.user)

        updated_data = {
            'name': 'Updated Team Name',
            'members': [self.user.id]
        }

        response = self.client.post(reverse('edit_team', kwargs={'team_id': team.id}), updated_data)
        
        self.assertEqual(response.status_code, 302)       # Check for successful redirect
        team.refresh_from_db()                            # Refresh the team object from the database
        
        self.assertEqual(team.name, 'Updated Team Name')  # Check if team name was updated

class DeleteTeamTestCase(TestCase):

    # Set up for testing
    def setUp(self):

        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username="TestUser", 
            email="test@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.user2 = CustomUser.objects.create_user(
            username="TestUser2", 
            email="test2@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True  # Assuming this is a team league
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)
        LeagueMembership.objects.create(player=self.user2, league=self.league)

    # Test that user can delete team
    def test_delete_team(self):
        self.client.login(username='TestUser', password='top_secret')

        team = Team.objects.create(name='Test Team', league=self.league)
        team.members.add(self.user)

        response = self.client.post(reverse('delete_team', kwargs={'team_id': team.id}))

        self.assertEqual(response.status_code, 302)                 # Check for successful redirect after deletion
        self.assertFalse(Team.objects.filter(id=team.id).exists())  # Check if team was deleted

class CreateMatchTestCase(TestCase):

   # Set up for testing
    def setUp(self):

        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username="TestUser", 
            email="test@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.user2 = CustomUser.objects.create_user(
            username="TestUser2", 
            email="test2@gmail.com", 
            password="top_secret", 
            account_bio="hi",
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True  # Assuming this is a team league
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)
        LeagueMembership.objects.create(player=self.user2, league=self.league)

        self.team1 = Team.objects.create(league=self.league, name='Team 1')
        self.team2 = Team.objects.create(league=self.league, name='Team 2')

    # Test that matches can be created
    def test_create_match(self):
            
            self.client.login(username='TestUser', password='top_secret')

            data = {
                'date': '2024-01-01 12:00:00',
                'player1': self.user.id,
                'player2': self.user2.id,
                'player1_score': 2,
                'player2_score': 1
            }

            url = reverse('create_match', kwargs={'league_id': self.league.id})
            response = self.client.post(url, data, follow=True)

            self.assertEqual(response.status_code, 200)                                                     # Check for successful creation 
            self.assertRedirects(response, reverse('league_detail', kwargs={'league_id': self.league.id}))  # Check for redirection

            # Check that the match exists in the database
            created_match = Match.objects.filter(league=self.league, player1=self.user, player2=self.user2).first()
            self.assertIsNotNone(created_match)
            self.assertEqual(created_match.player1_score, 2)
            self.assertEqual(created_match.player2_score, 1)
            self.assertEqual(created_match.date.strftime('%Y-%m-%d %H:%M:%S'), '2024-01-01 12:00:00')

class CreateTeamMatchTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username="TestUser",
            email="test@gmail.com",
            password="top_secret",
            account_bio="hi",
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True  # Assuming this is a team league
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)

        self.team1 = Team.objects.create(league=self.league, name='Team 1')
        self.team2 = Team.objects.create(league=self.league, name='Team 2')

    def test_create_match(self):
        self.client.login(username='TestUser', password='top_secret')

        data = {
            'date': '2024-01-01 12:00:00',
            'team1': self.team1.id,
            'team2': self.team2.id,
            'team1_score': 2,
            'team2_score': 1
        }

        url = reverse('create_match', kwargs={'league_id': self.league.id})
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)                                                     # Check for successful creation 
        self.assertRedirects(response, reverse('league_detail', kwargs={'league_id': self.league.id}))  # Check for redirection

        # Check that the match exists in the database
        created_match = Match.objects.filter(league=self.league, team1=self.team1, team2=self.team2).first()
        self.assertIsNotNone(created_match)
        self.assertEqual(created_match.team1_score, 2)
        self.assertEqual(created_match.team2_score, 1)
        self.assertEqual(created_match.date.strftime('%Y-%m-%d %H:%M:%S'), '2024-01-01 12:00:00')

class ReadMatchTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username='TestUser',
            email='test@example.com',
            password='top_secret'
        )
        self.user2 = CustomUser.objects.create_user(
            username='TestUser2',
            email='test2@example.com',
            password='top_secret'
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)
        LeagueMembership.objects.create(player=self.user2, league=self.league)

        self.match = Match.objects.create(
            league=self.league,
            date='2024-01-01 12:00:00',
            player1=self.user,
            player2=self.user2,
            player1_score=2,
            player2_score=1
        )

    def test_view_match_detail(self):
        url = reverse('match_detail', kwargs={'match_id': self.match.id})
        response = self.client.get(url)

        # Check for successful retrieval of match detail
        self.assertEqual(response.status_code, 302)

class UpdateMatchTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username='TestUser',
            email='test@example.com',
            password='top_secret'
        )
        self.user2 = CustomUser.objects.create_user(
            username='TestUser2',
            email='test2@example.com',
            password='top_secret'
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)
        LeagueMembership.objects.create(player=self.user2, league=self.league)

        self.match = Match.objects.create(
            league=self.league,
            date='2024-01-01 12:00:00',
            player1=self.user,
            player2=self.user2,
            player1_score=2,
            player2_score=1
        )

    def test_update_match(self):

        self.client.login(username='TestUser', password='top_secret')

        data = {
            'date': '2024-08-08 12:00:00',
            'player1': self.user.id,
            'player2': self.user2.id,
            'player1_score': 4,
            'player2_score': 4
        }

        url = reverse('edit_match', kwargs={'match_id': self.match.id})
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)         # Check for successful update

        updated_match = Match.objects.get(id=self.match.id) # Refresh match from database

        # Check updated attributes
        self.assertEqual(updated_match.date.strftime('%Y-%m-%d %H:%M:%S'), '2024-08-08 12:00:00')
        self.assertEqual(updated_match.player1_score, data['player1_score'])
        self.assertEqual(updated_match.player2_score, data['player2_score'])

class UpdateTeamMatchTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username='TestUser',
            email='test@example.com',
            password='top_secret'
        )
        self.user2 = CustomUser.objects.create_user(
            username='TestUser2',
            email='test2@example.com',
            password='top_secret'
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)
        LeagueMembership.objects.create(player=self.user2, league=self.league)

        self.team1 = Team.objects.create(league=self.league, name='Team 1')
        self.team2 = Team.objects.create(league=self.league, name='Team 2')

    def test_update_match(self):

        self.client.login(username='TestUser', password='top_secret')

        data = {
            'date': '2024-08-08 12:00:00',
            'team1': self.team1.id,
            'team2': self.team2.id,
            'team1_score': 3,
            'team2_score': 2
        }

        url = reverse('edit_match', kwargs={'match_id': self.match.id})
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)         # Check for successful update

        updated_match = Match.objects.get(id=self.match.id) # Refresh match from database

        # Check updated attributes
        self.assertEqual(updated_match.date.strftime('%Y-%m-%d %H:%M:%S'), '2024-08-08 12:00:00')
        self.assertEqual(updated_match.team1_id, data['team1'])
        self.assertEqual(updated_match.team2_id, data['team2'])
        self.assertEqual(updated_match.team1_score, data['team1_score'])
        self.assertEqual(updated_match.team2_score, data['team2_score'])

class DeleteMatchTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username='TestUser',
            email='test@example.com',
            password='top_secret'
        )
        self.user2 = CustomUser.objects.create_user(
            username='TestUser2',
            email='test2@example.com',
            password='top_secret'
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)
        LeagueMembership.objects.create(player=self.user2, league=self.league)

        self.match = Match.objects.create(
            league=self.league,
            date='2024-01-01 12:00:00',
            player1=self.user,
            player2=self.user2,
            player1_score=4,
            player2_score=6
        )

    def test_delete_match(self):

        self.client.login(username='TestUser', password='top_secret')

        url = reverse('delete_match', kwargs={'match_id': self.match.id})
        response = self.client.post(url, follow=True)

        self.assertEqual(response.status_code, 200) # Check for successful deletion

        # Verify match is deleted
        with self.assertRaises(Match.DoesNotExist):
            Match.objects.get(id=self.match.id)

class DeleteTeamMatchTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username='TestUser',
            email='test@example.com',
            password='top_secret'
        )
        self.user2 = CustomUser.objects.create_user(
            username='TestUser2',
            email='test2@example.com',
            password='top_secret'
        )

        self.league = League.objects.create(
            name='Test League',
            description='This is a test league.',
            owner=self.user,
            team_league=True
        )
        LeagueMembership.objects.create(player=self.user, league=self.league)
        LeagueMembership.objects.create(player=self.user2, league=self.league)

        self.team1 = Team.objects.create(league=self.league, name='Team 1')
        self.team2 = Team.objects.create(league=self.league, name='Team 2')

        self.teammatch = Match.objects.create(
            league=self.league,
            date='2024-01-01 12:00:00',
            team1=self.team1,
            team2=self.team2,
            team1_score=2,
            team2_score=1
        )

    def test_delete_match(self):

        self.client.login(username='TestUser', password='top_secret')

        url = reverse('delete_match', kwargs={'match_id': self.teammatch.id})
        response = self.client.post(url, follow=True)

        self.assertEqual(response.status_code, 200) # Check for successful deletion

        # Verify match is deleted
        with self.assertRaises(Match.DoesNotExist):
            Match.objects.get(id=self.teammatch.id)