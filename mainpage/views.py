from django.shortcuts import render
from django.http import HttpResponse
import requests

def home(request):
    return HttpResponse("<h1>홈 페이지가 곧 나타납니다 🚀</h1>")


# API에서 영화 데이터 가져오기
def fetch_movies_from_api():
    url = "http://43.200.28.219:1313/movies/"
    response = requests.get(url)
    movies_data = response.json().get('movies', [])
    return movies_data


# 외부 API 데이터를 DB에 초기 저장
def init_db(request):
    movies = fetch_movies_from_api()
    for item in movies:
        Movie.objects.create(
            title_kor=item['title_kor'],
            poster_url=item['poster_url']
        )
    return HttpResponse("DB 초기화 완료!")


from django.http import JsonResponse
from .models import Movie

def movie_list(request):
    movies = Movie.objects.all()

    data = [
        {
            "title_kor": movie.title_kor,
            "poster_url": movie.poster_url
        }
        for movie in movies
    ]

    response = {
        "movies": data
    }

    return JsonResponse(response)



