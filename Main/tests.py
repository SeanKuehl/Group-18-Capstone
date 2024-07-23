from django.http import request
from django.test import Client, RequestFactory, TestCase, client
from django.urls import reverse
from Main.models import *
from Accounts.models import CustomUser
from notifications.models import Notification
from django.utils import timezone

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
        response = self.client.get(reverse("remove_account", kwargs={'pk':self.removable_user.id}))
        
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


class PostViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.client.login(username='jacob', password='top_secret')
        
        self.post = Post.objects.create(
            accountname=self.user,
            post_title="Sample Post",
            post_community="General",
            post_body="This is a sample post body."
        )
    
    def test_view_posts(self):
        response = self.client.get(reverse("post_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.post_title)

    def test_view_post_detail(self):
        response = self.client.get(reverse("post_detail", kwargs={'pk': self.post.id, 'action': 0}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.post_title)

class PostCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.client.login(username='jacob', password='top_secret')

    def test_create_post(self):
        response = self.client.post(reverse("post_index"), {
            "post_title": "New Post",
            "post_community": "Community",
            "post_body": "Post body content.",
        })
        
        self.assertEqual(response.status_code, 302)  # Assuming a redirect happens on success
        self.assertTrue(Post.objects.filter(post_title="New Post").exists())

class PostSearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.client.login(username='jacob', password='top_secret')

        self.post = Post.objects.create(
            accountname=self.user,
            post_title="Searchable Post",
            post_community="Community",
            post_body="This post should be searchable.",
        )

    def test_search_posts(self):
        response = self.client.get(reverse("search_results") + "?q=Searchable")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.post_title)

class AddTagTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.client.login(username='jacob', password='top_secret')

        self.tag = Tag.objects.create(name="Test Tag")
        self.post = Post.objects.create(
            accountname=self.user,
            post_title="Tagged Post",
            post_community="Community",
            post_body="This post will be tagged.",
        )
        self.post.tags.add(self.tag)

    def test_add_tag(self):
        response = self.client.get(reverse("post_tag", kwargs={'tag': self.tag.name}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.post_title)

class CommentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.client.login(username='jacob', password='top_secret')

        self.post = Post.objects.create(
            accountname=self.user,
            post_title="Commentable Post",
            post_community="Community",
            post_body="This post will receive a comment.",
        )

    def test_make_comment(self):
        response = self.client.post(reverse("post_detail", kwargs={'pk': self.post.id, 'action': 0}), {
            "body": "This is a comment.",
        })
        
        self.assertEqual(response.status_code, 302)  # Assuming a redirect on success
        self.assertTrue(Comment.objects.filter(body="This is a comment.").exists())

class AccountHomePageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret", account_bio="wierdo",
        )
        self.client.login(username='jacob', password='top_secret')

    def test_account_homepage(self):
        response = self.client.get(reverse("user_account", kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

class CommentNotificationTests(TestCase):

    def setUp(self):
        # Create test users
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.mentioned_user = CustomUser.objects.create_user(username='mentioneduser', password='password')
        # Create a post
        self.post = Post.objects.create(title='Test Post', body='Test body', author=self.user)

    def test_notification_created_on_mention(self):
        # Simulate mentioning a user in a post
        self.post.body = f'@{self.mentioned_user.username} Check this out!'
        self.post.save()

        # Check if the notification is created
        notification = Notification.objects.filter(user=self.mentioned_user).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.text, f'You were mentioned in a post by {self.user.username}.')
        self.assertFalse(notification.read)
        self.assertTrue(notification.created_at <= timezone.now())

    def test_notification_created_on_comment(self):
        # Create a comment on the post
        comment = Comment.objects.create(post=self.post, author=self.commented_user, body='Great post!')
        
        # Check if the notification is created
        notification = Notification.objects.filter(user=self.user).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.text, f'{self.commented_user.username} commented on your post.')
        self.assertFalse(notification.read)
        self.assertTrue(notification.created_at <= timezone.now())