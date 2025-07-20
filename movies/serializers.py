from rest_framework import serializers
from .models import Movie, Actor

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['name', 'character', 'image_url']

'''
class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title_kor', 'title_eng', 'poster_url', 'genre',
            'showtime', 'release_date', 'plot', 'rating',
            'director_name', 'director_image_url', 'actors'
        ]
'''
class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title_kor', 'title_eng', 'poster_url', 'genre',
            'showtime', 'release_date', 'plot', 'audience_score',
            'director_name', 'director_image_url', 'actors'
        ]
