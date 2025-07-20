from rest_framework import serializers
from .models import Movie, Actor


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()  # 👈 optional

    class Meta:
        model = Movie
        fields = [
            'id',
            'title_kor',
            'title_eng',
            'poster_url',
            'genre',
            'showtime',
            'release_date',
            'plot',
            'director_name',
            'director_image_url',
            'audience_score',
            'critic_score',
            'netizen_score',
            'rating',  # 👈 optional
            'actors',
        ]

    def get_rating(self, obj):
        scores = [s for s in [obj.audience_score, obj.critic_score, obj.netizen_score] if s is not None]
        return round(sum(scores) / len(scores), 1) if scores else None