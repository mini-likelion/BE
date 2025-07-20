import requests
from django.http import JsonResponse
from .models import Movie, Actor
from .serializers import MovieSerializer, ActorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 🎥 전체 영화 목록 조회
@api_view(['GET'])
def movie_list(request):
    try:
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except Exception as e:
        print("🔥 movie_list 예외 발생:", repr(e))
        return Response({"error": str(e)}, status=500)

# 🎥 특정 영화 상세 조회
@api_view(['GET'])
def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=404)
    except Exception as e:
        print("🔥 movie_detail 예외 발생:", repr(e))
        return Response({"error": str(e)}, status=500)
