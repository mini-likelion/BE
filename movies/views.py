import requests
from django.http import JsonResponse
from .models import Movie, Actor
from .serializers import MovieSerializer, ActorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# 🔧 Swagger용 파라미터 명시 (선택 사항)
movie_id_param = openapi.Parameter(
    'movie_id', openapi.IN_PATH,
    description="영화 ID", type=openapi.TYPE_INTEGER
)

# 🎥 전체 영화 목록 조회
@api_view(['GET']) 
@swagger_auto_schema(
    method='get',
    operation_summary="전체 영화 목록 조회",
    responses={200: MovieSerializer(many=True)}
)
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
@swagger_auto_schema(
    method='get',
    operation_summary="특정 영화 상세 조회",
    manual_parameters=[movie_id_param],
    responses={200: MovieSerializer}
)
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

# 🔧 DB 초기화용 외부 API 가져오기 (문서화 제외)
def init_db(request):
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
                print("🎬 개별 영화 저장 중 에러:", inner_err)

        return JsonResponse({'message': '데이터 저장 완료'})
    except Exception as e:
        print("🚨 init_db 전체 에러:", e)
        return JsonResponse({'error': str(e)}, status=500)
