from django.urls import path
from .views import movie_list, movie_detail

app_name = 'movies'

urlpatterns = [
    path('', movie_list, name='movie-list'),               
    path('<int:movie_id>/', movie_detail, name='movie-detail'),
]