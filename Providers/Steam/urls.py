from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Main.urls')),
    path("steam/login/", views.steam_login, name="steam_login"),
    path("steam/callback/", views.steam_callback, name="steam_callback"),
]
