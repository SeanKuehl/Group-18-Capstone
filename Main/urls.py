"""
URL configuration for Testudo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import HomePage, SearchResultsView

urlpatterns = [
    path('post/', views.post_index, name="post_index"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("tag/<tag>/", views.post_tag, name="post_tag"),
    path('', HomePage.as_view(), name='home'),
    path("search/",SearchResultsView.as_view(), name="search_results"),
    path('create-account/', views.create_account, name='create_account'),
    path('search-account/', views.search_account, name='search_account'),
]
