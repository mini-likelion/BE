from django.urls import path
from .views import movie_list, movie_detail, init_db

app_name = 'movies'

urlpatterns = [    
    path('movies/', movie_list, name='movie-list'),
    path('movies/<int:movie_id>/', movie_detail, name='movie-detail'),
    path('init_db/', init_db, name='init-db'),
]