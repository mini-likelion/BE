import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


API_URL = "http://43.200.28.219:1313/movies/"


# 🎥 전체 영화 목록 조회 (외부 API 호출)
@api_view(['GET'])
def movie_list(request):
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        movies = res.json().get('movies', [])
        return Response(movies)
    except requests.RequestException as e:
        print("🔥 [movie_list] 외부 API 호출 실패:", repr(e))
        return Response({"error": "영화 목록을 가져오는 중 오류 발생"}, status=500)


# 🎥 특정 영화 상세 조회 (외부 API 호출)
@api_view(['GET'])
def movie_detail(request, movie_id):
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        movies = res.json().get('movies', [])
        
        if movie_id < 0 or movie_id >= len(movies):
            return Response({"error": "Movie not found"}, status=404)

        return Response(movies[movie_id])
    except requests.RequestException as e:
        print("🔥 [movie_detail] 외부 API 호출 실패:", repr(e))
        return Response({"error": "영화 상세 정보를 가져오는 중 오류 발생"}, status=500)
