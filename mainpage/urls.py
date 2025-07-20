from django.urls import path
from .views import movie_list
from . import views

app_name = 'mainpage'

urlpatterns = [
    path('', views.home),
    path('movies/', views.movie_list, name='movie_list'),
    path('init_db/', views.init_db, name='init_db'),
]

