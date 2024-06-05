from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_list(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})
