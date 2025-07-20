import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

API_URL = "http://43.200.28.219:1313/movies/"

# 🎥 전체 영화 목록 조회 (외부 API 호출)
@api_view(['GET'])
def movie_list(request):
    try:
        res = requests.get(API_URL)
        if res.status_code != 200:
            return Response({"error": "외부 API에서 데이터를 받아오지 못했습니다."}, status=500)
        
        movies = res.json().get('movies', [])
        return Response(movies)
    except Exception as e:
        print("🔥 movie_list 예외 발생:", repr(e))
        return Response({"error": str(e)}, status=500)

# 🎥 특정 영화 상세 조회 (외부 API 호출)
@api_view(['GET'])
def movie_detail(request, movie_id):
    try:
        res = requests.get(API_URL)
        if res.status_code != 200:
            return Response({"error": "외부 API에서 데이터를 받아오지 못했습니다."}, status=500)

        movies = res.json().get('movies', [])
        try:
            movie = movies[movie_id]  # 인덱스 기준 조회
        except IndexError:
            return Response({"error": "Movie not found"}, status=404)

        return Response(movie)
    except Exception as e:
        print("🔥 movie_detail 예외 발생:", repr(e))
        return Response({"error": str(e)}, status=500)

