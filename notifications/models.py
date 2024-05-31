from django.db import models
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.text}'
