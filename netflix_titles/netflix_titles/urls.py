"""netflix_titles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('movies/', views.movies, name='movies'),
    path('tvshows/', views.tvshows, name='tvshows'),
    path('search/', views.search, name='search'),
    path('add/', views.add, name='add'),
    path('year/', views.search_by_release_year, name='year'),
    path('edit/', views.edit, name='edit'),
    path('edit/<str:title>/', views.edit),
    path('person/', views.person, name='person'),
    path('person/<str:name>/', views.person),
    path('delmovie/', views.delete_movie, name='delmovie'),
    path('delmovie/<str:title>/', views.delete_movie),
    path('deltv/', views.delete_tvshow, name='deltv'),
    path('deltv/<str:title>/', views.delete_tvshow),
    path('country/', views.country, name='country'),
    path('work/', views.work, name='work')
]
