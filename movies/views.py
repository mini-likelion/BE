import requests
from django.http import JsonResponse
from .models import Movie, Actor
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Swagger 문서 자동화를 위한 데코레이터
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='get', responses={200: MovieSerializer(many=True)})
@api_view(['GET'])
def movie_list(request):
    """
    GET /movies/
    영화 전체 목록을 반환합니다.
    """
    try:
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except Exception as e:
        print("🔥 movie_list 에러:", e)
        return Response({"error": str(e)}, status=500)


@swagger_auto_schema(method='get', responses={200: MovieSerializer()})
@api_view(['GET'])
def movie_detail(request, movie_id):
    """
    GET /movies/<movie_id>/
    특정 영화 상세 정보를 반환합니다.
    """
    try:
        movie = Movie.objects.get(id=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)


# Swagger 문서에서는 제외할 관리용 DB 초기화 함수
def init_db(request):
    """
    GET /init_db/
    외부 API에서 영화 데이터를 불러와 저장합니다.
    Swagger 문서에는 노출되지 않습니다.
    """
    try:
        url = "http://43.200.28.219:1313/movies/"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        movies_data = res.json().get('movies', [])

        if not movies_data:
            return JsonResponse({'error': '영화 데이터가 없습니다'}, status=500)

        for m in movies_data:
            try:
                movie = Movie.objects.create(
                    title_kor=m.get('title_kor'),
                    title_eng=m.get('title_eng'),
                    poster_url=m.get('poster_url'),
                    genre=m.get('genre'),
                    showtime=m.get('showtime'),
                    release_date=m.get('release_date'),
                    plot=m.get('plot'),
                    audience_score=m.get('rating'),
                    director_name=m.get('director_name'),
                    director_image_url=m.get('director_image_url'),
                )

                for actor in m.get('actors', []):
                    Actor.objects.create(
                        movie=movie,
                        name=actor.get('name'),
                        character=actor.get('character'),
                        image_url=actor.get('image_url'),
                    )
            except Exception as inner_err:
                print("🎬 영화 저장 중 오류:", inner_err)

        return JsonResponse({'message': '데이터 저장 완료'})
    except Exception as e:
        print("🚨 init_db 전체 에러:", e)
        return JsonResponse({'error': str(e)}, status=500)

